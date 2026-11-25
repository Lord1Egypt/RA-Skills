#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猫适口性试验双盆数据分析脚本

输入：符合「猫适口性试验记录」模板的 .xlsx（含『原始记录单』sheet）
输出：cleaned_data.csv、analysis_results.xlsx、图表若干、report.md

统计口径（已与用户确认）：
- 采食量 = 单盆给料量 - 余料量（g）
- 对比数：同一猫同一餐，A采食 - B采食 >= 4g 记 A 胜 1 次；
  B采食 - A采食 >= 4g 记 B 胜 1 次；|差| < 4g 记平局，不计入胜负。
- 异常剔除双轨：① 备注含「待核/涂改/模糊/呕吐/软便/打翻/拒食/异常/混食/换人/位移」关键词；
  ② 每餐采食量按 IQR 1.5 倍检测离群。两者都记入剔除清单。
- 显著性：同一猫同一餐 A vs B 为配对数据。同时输出配对 t 检验与 Wilcoxon 符号秩检验；
  以 Shapiro-Wilk 正态性检验决定采用哪一种为主线结论。
- 首选率：首口料 == 'A料' / 'B料' 的记录计入对应首选；
  '同时采食'/'无采食'/'未观察' 不计入首选率分母。首选率 = A首选数 / (A首选数 + B首选数)。
- 平均顿采食量、顿采食中位数：按组/按餐，对有效记录的采食量(g)求均值与中位数。
"""

import argparse
import os
import sys
import re
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

# ==================== 可配置参数 ====================
SHEET_RAW = "原始记录单"
GROUP_NAMES = ["第一组", "第二组", "第三组"]
MEALS = ["第 1 餐", "第 2 餐", "第 3 餐", "第 4 餐", "第 5 餐"]
ABNORMAL_KEYWORDS = ["待核", "涂改", "模糊", "呕吐", "软便", "打翻", "拒食",
                     "异常", "混食", "换人", "位移", "设备异常", "未记录"]
WIN_DIFF_G = 4.0          # 对比数胜负阈值(g)
IQR_MULTIPLIER = 1.5      # IQR 离群倍数
IQR_MIN_N = 4             # 组内有效样本下限，低于此值不做 IQR（避免小样本误杀）
ALPHA = 0.05

MEAL_COLS = {
    1: {"A": 3, "B": 4, "first": 5, "pos": None},
    2: {"A": 6, "B": 7, "first": 8, "pos": None},
    3: {"A": 9, "B": 10, "first": 11, "pos": None},
    4: {"A": 12, "B": 13, "first": 14, "pos": None},
    5: {"A": 15, "B": 16, "first": 17, "pos": None},
}
# 位置行在 row 5（0-based），A左/A右，索引对应餐次的A列
POS_ROW_INDEX = 5
GROUP_ROW_A_INDEX = 7   # 每组首行是「对比料」行
COL_SEQ = 1             # 序号列
COL_CAT = 2             # 猫号列
COL_NOTE = 18           # 备注列
COL_GROUP = 0           # 组别列


def read_feeding_amount(ws):
    """从抬头读单盆给料量(g)。位于第3行(index=2)，遍历找数值。"""
    for row in ws.iter_rows(min_row=1, max_row=4, values_only=True):
        for v in row:
            if isinstance(v, (int, float)) and 5 <= float(v) <= 500:
                return float(v)
    return 40.0


def parse_position(ws):
    """解析每餐 A 料位置（A左/A右）。位置行 row5(index)。"""
    row = list(next(ws.iter_rows(min_row=6, max_row=6, values_only=True)))
    pos = {}
    for meal, cfg in MEAL_COLS.items():
        idx = cfg["A"]
        v = row[idx] if idx < len(row) else None
        if v and "A左" in str(v):
            pos[meal] = "A左"
        elif v and "A右" in str(v):
            pos[meal] = "A右"
        else:
            pos[meal] = "未知"
    return pos


def parse_abnormal(ws):
    """解析备注异常标记。key = 行号(0-based)，避免各组序号重复导致的串组覆盖。"""
    result = {}
    rows = list(ws.iter_rows(values_only=True))
    for r_idx in range(7, len(rows)):
        row = rows[r_idx]
        note = row[COL_NOTE] if len(row) > COL_NOTE else None
        seq = row[COL_SEQ]
        # 跳过分组标题行和签字行
        if seq in (None, "", "序号") or not isinstance(seq, (int, float)):
            continue
        if note:
            note_str = str(note)
            hits = [kw for kw in ABNORMAL_KEYWORDS if kw in note_str]
            if hits:
                result[r_idx] = hits
    return result


def parse_raw(ws):
    """解析原始记录单，返回长表 DataFrame（每行=一只猫一餐）。"""
    feeding = read_feeding_amount(ws)
    position = parse_position(ws)
    abnormal_map = parse_abnormal(ws)

    rows = list(ws.iter_rows(values_only=True))
    records = []
    current_group = None

    for r_idx in range(7, len(rows)):
        row = rows[r_idx]
        grp = row[COL_GROUP]
        seq = row[COL_SEQ]
        cat = row[COL_CAT]

        # 识别分组行（组别非空）
        if grp and str(grp).strip() in GROUP_NAMES:
            current_group = str(grp).strip()

        # 只处理数据行：序号为数字
        if not isinstance(seq, (int, float)) or isinstance(seq, bool):
            continue
        if current_group is None:
            continue

        note = row[COL_NOTE] if len(row) > COL_NOTE else None
        note_str = "" if note is None else str(note)
        seq_int = int(seq)
        remark_hit = abnormal_map.get(r_idx, [])

        for meal in range(1, 6):
            cfg = MEAL_COLS[meal]
            a_left = row[cfg["A"]]
            b_left = row[cfg["B"]]
            first = row[cfg["first"]]

            # 余料量缺失（空白）→ 记录但标缺失
            a_missing = a_left is None or a_left == ""
            b_missing = b_left is None or b_left == ""

            a_intake = None if a_missing else round(feeding - float(a_left), 2)
            b_intake = None if b_missing else round(feeding - float(b_left), 2)

            records.append({
                "组别": current_group,
                "序号": seq_int,
                "猫号": "" if cat is None else str(cat),
                "餐次": meal,
                "餐次名": MEALS[meal - 1],
                "位置": position.get(meal, "未知"),
                "余料A": None if a_missing else float(a_left),
                "余料B": None if b_missing else float(b_left),
                "采食A": a_intake,
                "采食B": b_intake,
                "首口料": "" if first is None else str(first).strip(),
                "备注": note_str,
                "备注异常关键词": ";".join(remark_hit),
            })

    df = pd.DataFrame(records)
    # 固定组序，避免 groupby 按字符串排序（第一组/第三组/第二组）
    df["组别"] = pd.Categorical(df["组别"], categories=GROUP_NAMES, ordered=True)
    return df, feeding, position


def flag_outliers_iqr(df):
    """按餐次+组别分别对 A/B 采食量做 IQR 1.5 倍离群检测。"""
    flags = set()  # (index) 需要剔除的行
    detail = []
    skipped = []
    for (grp, meal), sub in df.groupby(["组别", "餐次"]):
        for ab in ["A", "B"]:
            col = f"采食{ab}"
            s = sub[col].dropna()
            if len(s) < IQR_MIN_N:
                skipped.append(f"{grp}{MEALS[int(meal) - 1]} n={len(s)}")
                continue
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            lo, hi = q1 - IQR_MULTIPLIER * iqr, q3 + IQR_MULTIPLIER * iqr
            for idx, val in s.items():
                if val < lo or val > hi:
                    flags.add(idx)
                    detail.append({
                        "组别": grp, "餐次": meal, "猫号": df.loc[idx, "猫号"],
                        "指标": col, "数值": val,
                        "合理区间": f"[{lo:.2f}, {hi:.2f}]",
                        "原因": "IQR离群",
                    })
    return flags, detail, skipped


def clean_data(df):
    """双轨异常剔除，返回清洗后数据 + 剔除清单。"""
    df = df.copy()
    df["剔除原因"] = ""

    # 轨1：备注关键词
    remark_mask = df["备注异常关键词"] != ""
    df.loc[remark_mask, "剔除原因"] = df.loc[remark_mask, "备注异常关键词"].apply(
        lambda x: "备注:" + x)

    # 轨2：IQR
    iqr_flags, iqr_detail, iqr_skipped = flag_outliers_iqr(df)
    for idx in iqr_flags:
        cur = df.loc[idx, "剔除原因"]
        tag = "IQR离群"
        df.loc[idx, "剔除原因"] = tag if cur == "" else cur + ";" + tag

    # 缺失值：采食A或B为空也剔除
    miss_mask = df["采食A"].isna() | df["采食B"].isna()
    df.loc[miss_mask, "剔除原因"] = df.loc[miss_mask, "剔除原因"].apply(
        lambda x: "采食量缺失" if x == "" else x + ";采食量缺失")

    df["剔除"] = df["剔除原因"] != ""
    removed = df[df["剔除"]].copy()
    cleaned = df[~df["剔除"]].copy().reset_index(drop=True)
    return cleaned, removed, iqr_detail, iqr_skipped


def compute_win_counts(df):
    """对比数统计：按组、按猫、按餐。"""
    d = df.copy()
    d["采食差"] = (d["采食A"] - d["采食B"]).round(2)
    d["胜负"] = np.where(d["采食差"] >= WIN_DIFF_G, "A胜",
                       np.where(d["采食差"] <= -WIN_DIFF_G, "B胜", "平局"))

    # 按组别汇总
    grp = d.groupby("组别").agg(
        有效记录数=("胜负", "size"),
        A胜=("胜负", lambda s: (s == "A胜").sum()),
        B胜=("胜负", lambda s: (s == "B胜").sum()),
        平局=("胜负", lambda s: (s == "平局").sum()),
    ).reset_index()
    grp["A胜率"] = (grp["A胜"] / (grp["A胜"] + grp["B胜"])).round(4)

    # 按组×猫汇总
    cat = d.groupby(["组别", "猫号"]).agg(
        有效餐数=("胜负", "size"),
        A胜=("胜负", lambda s: (s == "A胜").sum()),
        B胜=("胜负", lambda s: (s == "B胜").sum()),
        平局=("胜负", lambda s: (s == "平局").sum()),
    ).reset_index()

    # 按组×餐汇总
    meal = d.groupby(["组别", "餐次"]).agg(
        有效记录数=("胜负", "size"),
        A胜=("胜负", lambda s: (s == "A胜").sum()),
        B胜=("胜负", lambda s: (s == "B胜").sum()),
        平局=("胜负", lambda s: (s == "平局").sum()),
    ).reset_index()

    return d, grp, cat, meal


def compute_preference(df_all, df_clean):
    """首选率统计。df_all 含全部有效（未剔除）记录用于分母说明。"""
    # 首选率基于清洗后的数据
    d = df_clean[df_clean["首口料"].isin(["A料", "B料"])].copy()
    d["首选"] = d["首口料"].map({"A料": "A", "B料": "B"})

    grp = d.groupby("组别").agg(
        有效首选数=("首选", "size"),
        A首选=("首选", lambda s: (s == "A").sum()),
        B首选=("首选", lambda s: (s == "B").sum()),
    ).reset_index()
    grp["A首选率"] = (grp["A首选"] / grp["有效首选数"]).round(4)
    grp["B首选率"] = (grp["B首选"] / grp["有效首选数"]).round(4)

    # 组×餐
    meal = d.groupby(["组别", "餐次"]).agg(
        有效首选数=("首选", "size"),
        A首选=("首选", lambda s: (s == "A").sum()),
        B首选=("首选", lambda s: (s == "B").sum()),
    ).reset_index()
    meal["A首选率"] = (meal["A首选"] / meal["有效首选数"]).round(4)
    meal["B首选率"] = (meal["B首选"] / meal["有效首选数"]).round(4)

    # 首口料分布（含同时/无采食/未观察）
    dist = df_clean.groupby(["组别", "首口料"]).size().unstack(fill_value=0).reset_index()
    return grp, meal, dist


def compute_intake_stats(df_clean):
    """平均顿采食量、顿采食中位数。"""
    rows = []
    for (grp, meal), sub in df_clean.groupby(["组别", "餐次"]):
        a = sub["采食A"].dropna()
        b = sub["采食B"].dropna()
        rows.append({
            "组别": grp, "餐次": meal,
            "有效记录数": min(len(a), len(b)),
            "平均顿采食A": round(a.mean(), 2) if len(a) else None,
            "平均顿采食B": round(b.mean(), 2) if len(b) else None,
            "顿采食中位数A": round(a.median(), 2) if len(a) else None,
            "顿采食中位数B": round(b.median(), 2) if len(b) else None,
            "标准差A": round(a.std(), 2) if len(a) > 1 else None,
            "标准差B": round(b.std(), 2) if len(b) > 1 else None,
        })
    meal_stats = pd.DataFrame(rows)

    rows2 = []
    for grp, sub in df_clean.groupby("组别"):
        a = sub["采食A"].dropna()
        b = sub["采食B"].dropna()
        rows2.append({
            "组别": grp, "有效记录数": min(len(a), len(b)),
            "平均顿采食A": round(a.mean(), 2) if len(a) else None,
            "平均顿采食B": round(b.mean(), 2) if len(b) else None,
            "顿采食中位数A": round(a.median(), 2) if len(a) else None,
            "顿采食中位数B": round(b.median(), 2) if len(b) else None,
        })
    grp_stats = pd.DataFrame(rows2)
    return grp_stats, meal_stats


def compute_significance(df_clean):
    """配对显著性分析：配对 t + Wilcoxon + 正态性。"""
    results = []
    for grp, sub in df_clean.groupby("组别"):
        pair = sub[["采食A", "采食B"]].dropna()
        a, b = pair["采食A"].values, pair["采食B"].values
        diff = a - b
        n = len(diff)

        # 正态性（对差值）
        if n >= 3:
            sh_stat, sh_p = stats.shapiro(diff)
        else:
            sh_stat, sh_p = np.nan, np.nan

        # 配对 t
        t_stat, t_p = stats.ttest_rel(a, b)
        # Cohen's d（配对）
        d_z = diff.mean() / diff.std(ddof=1) if diff.std(ddof=1) > 0 else np.nan

        # Wilcoxon 符号秩
        try:
            w_stat, w_p = stats.wilcoxon(a, b, zero_method="wilcox", correction=False)
        except ValueError:
            w_stat, w_p = np.nan, np.nan

        primary = "配对t检验" if sh_p >= ALPHA else "Wilcoxon符号秩检验"
        results.append({
            "组别": grp, "N": n,
            "A均值": round(a.mean(), 3), "B均值": round(b.mean(), 3),
            "均值差(A-B)": round(diff.mean(), 3),
            "Shapiro_W": round(sh_stat, 4) if not np.isnan(sh_stat) else None,
            "Shapiro_p": round(sh_p, 4) if not np.isnan(sh_p) else None,
            "t": round(t_stat, 4), "t_p": round(t_p, 4),
            "Cohens_dz": round(d_z, 4) if not np.isnan(d_z) else None,
            "Wilcoxon_W": round(w_stat, 2) if not np.isnan(w_stat) else None,
            "Wilcoxon_p": round(w_p, 4) if not np.isnan(w_p) else None,
            "主结论方法": primary,
            "显著性": "显著" if (t_p < ALPHA if primary == "配对t检验" else w_p < ALPHA) else "不显著",
        })
    return pd.DataFrame(results)


def compute_position_bias(df_clean):
    """左右位置偏倚校验。"""
    d = df_clean[df_clean["首口料"].isin(["A料", "B料"])].copy()
    d["A首选"] = (d["首口料"] == "A料").astype(int)
    pos = d.groupby("位置")["A首选"].agg(["mean", "size"]).reset_index()
    pos.columns = ["位置", "A首选率", "记录数"]
    left = pos[pos["位置"] == "A左"]["A首选率"].values
    right = pos[pos["位置"] == "A右"]["A首选率"].values
    bias = abs(left[0] - right[0]) if len(left) and len(right) else np.nan
    return pos, bias


def make_plots(df, win_grp, pref_grp, intake_meal, sig_df, out_dir):
    """生成可视化图表。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    colors = ["#4A90D9", "#E67E22"]

    charts = []

    # 1. 各组对比数柱状图
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(win_grp))
    w = 0.35
    ax.bar(x - w/2, win_grp["A胜"], w, label="A胜", color=colors[0])
    ax.bar(x + w/2, win_grp["B胜"], w, label="B胜", color=colors[1])
    ax.set_xticks(x)
    ax.set_xticklabels(win_grp["组别"])
    ax.set_ylabel("次数")
    ax.set_title(f"各组对比数（采食差≥{WIN_DIFF_G:g}g 判定胜负）")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    p = os.path.join(out_dir, "图1_对比数柱状图.png")
    plt.savefig(p, dpi=150); plt.close()
    charts.append(p)

    # 2. 各组首选率
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - w/2, pref_grp["A首选率"], w, label="A首选率", color=colors[0])
    ax.bar(x + w/2, pref_grp["B首选率"], w, label="B首选率", color=colors[1])
    ax.set_xticks(x); ax.set_xticklabels(pref_grp["组别"])
    ax.set_ylabel("首选率"); ax.set_ylim(0, 1.05)
    ax.set_title("各组首选率（A料 vs B料）")
    ax.legend(); ax.axhline(0.5, color="gray", linestyle="--", linewidth=1)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    p = os.path.join(out_dir, "图2_首选率柱状图.png")
    plt.savefig(p, dpi=150); plt.close()
    charts.append(p)

    # 3. 平均顿采食量（组×餐 折线）
    fig, ax = plt.subplots(figsize=(9, 5))
    for grp in intake_meal["组别"].unique():
        sub = intake_meal[intake_meal["组别"] == grp]
        ax.plot(sub["餐次"], sub["平均顿采食A"], marker="o", label=f"{grp}-A")
        ax.plot(sub["餐次"], sub["平均顿采食B"], marker="s", linestyle="--", label=f"{grp}-B")
    ax.set_xlabel("餐次"); ax.set_ylabel("平均顿采食量(g)")
    ax.set_title("各组各餐平均顿采食量")
    ax.legend(ncol=3, fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    p = os.path.join(out_dir, "图3_平均顿采食量折线.png")
    plt.savefig(p, dpi=150); plt.close()
    charts.append(p)

    # 4. 顿采食中位数（组×餐）
    fig, ax = plt.subplots(figsize=(9, 5))
    for grp in intake_meal["组别"].unique():
        sub = intake_meal[intake_meal["组别"] == grp]
        ax.plot(sub["餐次"], sub["顿采食中位数A"], marker="o", label=f"{grp}-A")
        ax.plot(sub["餐次"], sub["顿采食中位数B"], marker="s", linestyle="--", label=f"{grp}-B")
    ax.set_xlabel("餐次"); ax.set_ylabel("顿采食中位数(g)")
    ax.set_title("各组各餐顿采食中位数")
    ax.legend(ncol=3, fontsize=8)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    p = os.path.join(out_dir, "图4_顿采食中位数折线.png")
    plt.savefig(p, dpi=150); plt.close()
    charts.append(p)

    # 5. A/B 采食量配对箱线图（按组）
    fig, ax = plt.subplots(figsize=(9, 5))
    data_a = [df[df["组别"] == g]["采食A"].dropna().values for g in win_grp["组别"]]
    data_b = [df[df["组别"] == g]["采食B"].dropna().values for g in win_grp["组别"]]
    positions = np.arange(len(win_grp))
    bp_a = ax.boxplot(data_a, positions=positions - 0.2, widths=0.35,
                      patch_artist=True, tick_labels=list(win_grp["组别"]))
    bp_b = ax.boxplot(data_b, positions=positions + 0.2, widths=0.35,
                      patch_artist=True, tick_labels=list(win_grp["组别"]))
    for patch in bp_a["boxes"]: patch.set_facecolor(colors[0]); patch.set_alpha(0.7)
    for patch in bp_b["boxes"]: patch.set_facecolor(colors[1]); patch.set_alpha(0.7)
    ax.set_ylabel("采食量(g)"); ax.set_title("各组 A/B 采食量分布（清洗后）")
    ax.legend([bp_a["boxes"][0], bp_b["boxes"][0]], ["A料", "B料"])
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout()
    p = os.path.join(out_dir, "图5_AB采食量箱线图.png")
    plt.savefig(p, dpi=150); plt.close()
    charts.append(p)

    return charts


def write_report(out_dir, df_raw, df_clean, removed, iqr_detail,
                 win_grp, pref_grp, intake_grp, sig_df, pos_df, pos_bias,
                 feeding, position, charts):
    """生成 Markdown 报告。"""
    lines = []
    lines.append("# 猫适口性试验统计分析报告\n")
    lines.append(f"- 单盆给料量：{feeding:g} g")
    lines.append("- 位置安排：" + " / ".join(
        f"{MEALS[m - 1]} {position.get(m, '未知')}" for m in sorted(position)))
    lines.append(f"- 对比数阈值：采食差 ≥ {WIN_DIFF_G:g} g 判定胜负\n")

    lines.append("## 一、数据清洗\n")
    lines.append(f"- 原始记录：{len(df_raw)} 条（{len(df_raw)//5} 只猫 × 5 餐）")
    lines.append(f"- 剔除：{len(removed)} 条")
    lines.append(f"- 有效：{len(df_clean)} 条\n")
    if len(removed):
        lines.append("### 剔除清单\n")
        cols = ["组别", "序号", "猫号", "餐次", "采食A", "采食B", "首口料", "剔除原因"]
        lines.append(removed[[c for c in cols if c in removed.columns]].to_markdown(index=False))
        lines.append("")
    if iqr_detail:
        lines.append("### IQR 离群明细\n")
        lines.append(pd.DataFrame(iqr_detail).to_markdown(index=False))
        lines.append("")

    lines.append("## 二、对比数统计\n")
    lines.append("判定规则：A采食−B采食 ≥ 4g 记 A胜；B采食−A采食 ≥ 4g 记 B胜；|差|<4g 平局。\n")
    lines.append(win_grp.to_markdown(index=False))
    lines.append("")

    lines.append("## 三、显著性分析（配对数据 A vs B）\n")
    for _, r in sig_df.iterrows():
        lines.append(f"### {r['组别']}")
        lines.append(f"- 有效配对 N = {r['N']}，A均值 {r['A均值']}g，B均值 {r['B均值']}g，均值差 {r['均值差(A-B)']}g")
        lines.append(f"- 差值正态性 Shapiro-Wilk：W = {r['Shapiro_W']}, p = {r['Shapiro_p']}")
        lines.append(f"- 配对 t 检验：t = {r['t']}, p = {r['t_p']}, Cohen's dz = {r['Cohens_dz']}")
        lines.append(f"- Wilcoxon 符号秩：W = {r['Wilcoxon_W']}, p = {r['Wilcoxon_p']}")
        lines.append(f"- **主结论（{r['主结论方法']}）：{r['显著性']}**\n")

    lines.append("## 四、首选率分析\n")
    lines.append("分母 = A首选 + B首选；同时采食/无采食/未观察不计入。\n")
    lines.append(pref_grp.to_markdown(index=False))
    lines.append("")

    lines.append("## 五、平均顿采食量与顿采食中位数\n")
    lines.append(intake_grp.to_markdown(index=False))
    lines.append("")

    lines.append("## 六、左右位置偏倚校验\n")
    lines.append(pos_df.to_markdown(index=False))
    lines.append(f"\n位置偏倚指数 = {pos_bias:.4f}" if not np.isnan(pos_bias) else "\n位置偏倚指数：无法计算")
    lines.append("（≤5%：无偏倚；5%~10%：需关注；>10%：须在报告说明或增加餐次重测）\n")

    lines.append("## 七、可视化图表\n")
    for p in charts:
        lines.append(f"- {os.path.basename(p)}")

    path = os.path.join(out_dir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def write_excel(out_dir, win_grp, win_cat, win_meal, pref_grp, pref_meal,
                pref_dist, intake_grp, intake_meal, sig_df, pos_df,
                df_clean, removed, iqr_detail):
    """汇总结果 Excel。"""
    path = os.path.join(out_dir, "analysis_results.xlsx")
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        sig_df.to_excel(w, sheet_name="显著性分析", index=False)
        win_grp.to_excel(w, sheet_name="对比数_按组", index=False)
        win_cat.to_excel(w, sheet_name="对比数_按猫", index=False)
        win_meal.to_excel(w, sheet_name="对比数_按餐", index=False)
        pref_grp.to_excel(w, sheet_name="首选率_按组", index=False)
        pref_meal.to_excel(w, sheet_name="首选率_按餐", index=False)
        pref_dist.to_excel(w, sheet_name="首口料分布", index=False)
        intake_grp.to_excel(w, sheet_name="采食量_按组", index=False)
        intake_meal.to_excel(w, sheet_name="采食量_按餐", index=False)
        pos_df.to_excel(w, sheet_name="位置偏倚", index=False)
        df_clean.to_excel(w, sheet_name="清洗后数据", index=False)
        removed.to_excel(w, sheet_name="剔除清单", index=False)
        if iqr_detail:
            pd.DataFrame(iqr_detail).to_excel(w, sheet_name="IQR离群明细", index=False)
    return path


def main():
    global WIN_DIFF_G
    parser = argparse.ArgumentParser(description="猫适口性试验双盆数据分析")
    parser.add_argument("input", help="输入 xlsx 路径（含『原始记录单』sheet）")
    parser.add_argument("-o", "--output", default=None, help="输出目录，默认 ./palatability_output")
    parser.add_argument("--win-diff", type=float, default=WIN_DIFF_G, help="对比数胜负阈值(g)，默认4")
    args = parser.parse_args()

    WIN_DIFF_G = args.win_diff
    out_dir = args.output or os.path.join(os.getcwd(), "palatability_output")
    os.makedirs(out_dir, exist_ok=True)

    print(f"[1/7] 读取 {args.input}")
    import openpyxl
    wb = openpyxl.load_workbook(args.input, data_only=True)
    if SHEET_RAW not in wb.sheetnames:
        raise ValueError(f"未找到 sheet「{SHEET_RAW}」，实际有：{wb.sheetnames}")
    ws = wb[SHEET_RAW]
    df_raw, feeding, position = parse_raw(ws)
    print(f"      原始记录 {len(df_raw)} 条，给料量 {feeding}g")

    print("[2/7] 异常剔除（备注 + IQR 双轨）")
    df_clean, removed, iqr_detail, iqr_skipped = clean_data(df_raw)
    print(f"      剔除 {len(removed)} 条，有效 {len(df_clean)} 条")
    if iqr_skipped:
        combos = {x.split(" n=")[0] for x in iqr_skipped}
        print(f"      [警告] {len(combos)} 个「组×餐」组合样本量 < {IQR_MIN_N}，未执行 IQR 离群检测")

    print("[3/7] 对比数统计")
    df_scored, win_grp, win_cat, win_meal = compute_win_counts(df_clean)

    print("[4/7] 首选率统计")
    pref_grp, pref_meal, pref_dist = compute_preference(df_raw, df_clean)

    print("[5/7] 采食量描述统计 + 显著性")
    intake_grp, intake_meal = compute_intake_stats(df_clean)
    sig_df = compute_significance(df_clean)
    pos_df, pos_bias = compute_position_bias(df_clean)

    print("[6/7] 生成图表")
    charts = make_plots(df_clean, win_grp, pref_grp, intake_meal, sig_df, out_dir)
    print(f"      {len(charts)} 张图表")

    print("[7/7] 输出报告与汇总表")
    df_clean.to_csv(os.path.join(out_dir, "cleaned_data.csv"), index=False, encoding="utf-8-sig")
    removed.to_csv(os.path.join(out_dir, "removed_data.csv"), index=False, encoding="utf-8-sig")
    excel_path = write_excel(out_dir, win_grp, win_cat, win_meal, pref_grp, pref_meal,
                             pref_dist, intake_grp, intake_meal, sig_df, pos_df,
                             df_clean, removed, iqr_detail)
    report_path = write_report(out_dir, df_raw, df_clean, removed, iqr_detail,
                               win_grp, pref_grp, intake_grp, sig_df, pos_df, pos_bias,
                               feeding, position, charts)
    print(f"\n完成。输出目录：{out_dir}")
    print(f"  报告：{report_path}")
    print(f"  汇总：{excel_path}")


if __name__ == "__main__":
    main()
