#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v2.3 新图型模块：funnel / bland_altman / pca / paired / venn / cluster_heatmap。

由 gen_figure.py 在启动时 import 并合并进 GENERATORS/DEMO_DATA；
校验与 alt 文本经 validate_extra()/alt_extra() 钩子接入。
仅依赖 numpy + matplotlib + af_v23_stats。
"""
from __future__ import annotations

import sys

import numpy as np

try:
    import af_v23_stats as st
except ImportError:  # 同目录运行时直接可用；打包路径异常时显式报错
    raise

MAX_CLUSTER_ROWS = 3000   # linkage O(n²) 内存护栏
MAX_PCA_COLS = 200        # 特征列护栏


def _has_cjk(text):
    if not isinstance(text, str):
        return False
    return any('\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f'
               for ch in text)


def _fp(cjk_fp, text):
    return cjk_fp if (cjk_fp is not None and _has_cjk(str(text))) else None


def _warn(msg):
    print(f"WARNING: {msg}", file=sys.stderr)


# ── funnel 漏斗图 ─────────────────────────────────────────────────────

def gen_funnel(data, ax, theme, cjk_fp, **kwargs):
    """Meta 分析漏斗图：研究效应散点 + 合并效应竖线 + 95% 伪置信漏斗线。

    数据: {"studies": [{"name": "Smith 2020", "effect": 0.69, "se": 0.12}, ...]}
    或 {"effects": [...], "ses": [...], "labels": [...] }（效应建议为 log 尺度）。
    选项: egger=True 画 Egger 回归线（stderr 报告不对称检验 p）。
    """
    names, es, ses = _meta_studies(data, "funnel", hint="漏斗对称性目测不可靠")

    pooled = st.dl_pool(es, ses)
    c_main = theme["colors"][0]

    ax.scatter(es, ses, s=36, color=c_main, edgecolor="#333333",
               linewidth=0.8, zorder=4)
    se_max = float(ses.max()) * 1.08
    se_min = 0.0
    # 95% 伪置信漏斗
    for sign in (-1.0, 1.0):
        ax.plot([pooled["pooled"] - 1.96 * se_max, pooled["pooled"],
                 pooled["pooled"] + 1.96 * se_max],
                [se_max, se_min, se_max],
                color="#888888", linewidth=1.2, linestyle="--", zorder=2)
    ax.axvline(pooled["pooled"], color=c_main, linewidth=1.4, linestyle="-",
               alpha=0.85, zorder=3,
               label=f"合并效应 {pooled['pooled']:.3g}")
    ax.axvline(0, color="#BBBBBB", linewidth=0.8, zorder=1)
    ax.invert_yaxis()
    ax.set_ylabel("标准误 se")
    ax.set_xlabel("效应值")

    if kwargs.get("egger"):
        if len(es) >= 3:
            eg = st.egger_test(es, ses)
            # Egger 线：z = intercept + slope * (1/se) → effect = intercept*se + slope
            se_grid = np.linspace(se_min, se_max, 32)
            ax.plot(eg["slope"] + eg["intercept"] * se_grid, se_grid,
                    color=theme["colors"][1 % len(theme["colors"])],
                    linewidth=1.2, linestyle=":", zorder=3,
                    label=f"Egger 回归线 (P={eg['p']:.3g})")
            _warn(f"funnel: Egger 不对称检验 P={eg['p']:.4g}（截距 {eg['intercept']:.3g}）")
        else:
            _warn("funnel: Egger 检验需要 >=3 个研究，已跳过")
    ax.legend(fontsize=theme["font_size"] - 1, loc="upper right", framealpha=0.9,
              prop=cjk_fp if _has_cjk("".join(names)) or cjk_fp and _has_cjk(str(data.get("title", ""))) else None)
    _warn(f"funnel: DL 随机效应合并 {pooled['pooled']:.4g}（95%CI {pooled['pooled']-1.96*pooled['se']:.3g}~"
          f"{pooled['pooled']+1.96*pooled['se']:.3g}），异质性 I²={pooled['i2']:.0f}%，P_het={pooled['p_het']:.3g}")
    return None


def _meta_studies(data, tname, hint=""):
    """funnel/galbraith 共用的 Meta 研究数据解析。

    接受 studies[]（每项 name/effect/se）或 effects+ses 平行数组；校验数量一致、
    se 为正且有限；<5 个研究给统计效力警告。返回 (names, es, ses) ndarray。"""
    studies = data.get("studies", None)
    if studies:
        names = [str(s.get("name", f"研究{i+1}")) for i, s in enumerate(studies)]
        es = [float(s["effect"]) for s in studies]
        ses = [float(s["se"]) for s in studies]
    else:
        es = data.get("effects", data.get("effects_list", None))
        ses = data.get("ses", data.get("se_list", None))
        names = list(data.get("labels", []))
        if es is None or ses is None:
            raise ValueError(
                f"{tname}: 需要 'studies'（每项含 name/effect/se）或 'effects'+'ses' 数组 — "
                "森林图的 effect/lci/uci 格式请先换算（se≈(uci−lci)/3.92）")
    if len(es) != len(ses) or len(es) == 0:
        raise ValueError(f"{tname}: effects({len(es)}) 与 ses({len(ses)}) 数量不一致或为空")
    es = np.asarray(es, float)
    ses = np.asarray(ses, float)
    bad = ~(np.isfinite(es) & np.isfinite(ses) & (ses > 0))
    if bad.any():
        raise ValueError(f"{tname}: {int(bad.sum())} 个研究的 se 非法（必须为正且有限）")
    if len(es) < 5:
        _warn(f"{tname}: 仅 {len(es)} 个研究，{hint}（建议 >=10）")
    return names, es, ses


# ── galbraith Galbraith 径向图（v5.6 第 36 号图型，漏斗图姊妹图） ─────

_RATIO_LABELS = ("OR", "HR", "RR")


def _draw_galbraith_arcs(ax, b, x_hi, est_label, fs_s, cjk_fp, pts=None):
    """比率尺度效应量弧线：以原点为心的虚线圆弧，标注合并线上 OR/HR/RR 读数。

    目标效应 v → log 值 m，与合并线 y=bx 交于 x=m/b；只画与合并方向同侧、
    落在数据精度范围内的弧（MD/SMD 已在上层自动关闭）。
    标签放弧段中点并向外径向偏移（数据点簇集在合并线上，交点处必撞名——
    v5.6 视觉验收教训）；与任何研究点过近的标签整条弃标（弧线仍在）。"""
    import matplotlib.patches as mpatches
    if b == 0:
        _warn("galbraith: 合并效应为 0，效应量弧线无法定位，已跳过")
        return
    skipped = 0
    for v in (0.125, 0.25, 0.5, 1, 2, 4, 8, 16):
        m = float(np.log(v))
        x_m = m / b
        if not (0 < x_m <= x_hi):
            continue
        r = float(np.hypot(x_m, m))
        ang = float(np.degrees(np.arctan2(m, x_m)))
        # 标签位=弧段中点（ang−14°）再径向外推 12%——离开数据线簇集区
        import math as _m
        _a = _m.radians(ang - 14.0)
        lx, ly = 1.12 * r * _m.cos(_a), 1.12 * r * _m.sin(_a)
        # v5.7.0 交付验收裁决：弧线与读数同生共死——读数放不下时整条弧线
        # 一并省略（无读数的弧线对读者是无法判读的噪声；stderr 报告条数）
        if pts is not None and len(pts):
            _dx = np.array([lx - px for px, _ in pts])
            _dy = np.array([ly - pz for _, pz in pts])
            # v5.7：最小间距 0.10→0.075（读数密度放宽，仍以碰撞检测兜底防叠印）
            _near = float(np.hypot(x_hi, 1.0)) * 0.075  # 归一化最小间距（轴跨度 7.5%）
            if bool((np.hypot(_dx, _dy) < _near).any()):
                skipped += 1
                continue
        ax.add_patch(mpatches.Arc((0, 0), 2 * r, 2 * r, theta1=ang - 26.0,
                                  theta2=ang + 26.0, color="#999999",
                                  lw=0.9, linestyle=":", zorder=2))
        ax.annotate(f"{est_label}={v:g}", (lx, ly), ha="center", va="center",
                    fontsize=fs_s, color="#666666",
                    fontproperties=cjk_fp if cjk_fp and _has_cjk(est_label) else None)
    if skipped:
        _warn(f"galbraith: {skipped} 条效应量弧线（含读数）与研究名过近已整条省略"
              "（保留的弧线均带读数）")


def _declutter_annotations(ax, anns):
    """研究名标注去叠印（v5.6 视觉验收机制；类级铁律「相邻标注以画布完整性优先」）。

    逐个用真实像素框检测：与已放置标注重叠者翻到数据点下方重试；
    仍重叠则弃标（离群项例外——信息优先保留原位）。返回弃标数。
    anns 项 = (标注对象, 是否离群, 名, x, y, (dx,dy)offset, ha, 字号, 颜色, fp)"""
    if len(anns) < 2:
        return 0
    import matplotlib.patheffects as _pe
    _stroke = [_pe.withStroke(linewidth=2.2, foreground="white")]
    fig = ax.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    placed = []
    dropped = 0
    for a, is_out, nm, xi, zi, (dx, dy), ha, fs, color, fp in anns:
        bb = a.get_window_extent(renderer).expanded(1.12, 1.50)
        if not any(bb.overlaps(p) for p in placed):
            placed.append(bb)
            continue
        a.remove()
        # 候选位序列（real2 视觉验收两轮 fail 教训：仅纵向加深不够——
        # 双离群纵向互堵时需横向镜像候选；正下方、正下更深、左下×2、上方加深）
        _ha_m = "right" if ha == "left" else "left"
        _cands = tuple((dx, -abs(dy) - _d, ha, "top") for _d in (18, 27, 36, 48, 62, 80, 104, 132)) \
                 + tuple((-dx - 2, -abs(dy) - _d, _ha_m, "top") for _d in (18, 48)) \
                 + ((dx, abs(dy) + 6, ha, "bottom"),)
        a2 = None
        bb2 = None
        for _ox, _oy, _ha2, _va2 in _cands:
            a2 = ax.annotate(nm, (xi, zi), textcoords="offset points",
                             xytext=(_ox, _oy), ha=_ha2, va=_va2,
                             fontsize=fs, color=color, fontproperties=fp,
                             path_effects=_stroke, zorder=6)
            bb2 = a2.get_window_extent(renderer).expanded(1.12, 1.50)
            if not any(bb2.overlaps(p) for p in placed):
                break
            a2.remove()
            a2 = None
        if a2 is not None:
            placed.append(bb2)
        elif is_out:
            _re = ax.annotate(nm, (xi, zi), textcoords="offset points",
                              xytext=(dx, dy), ha=ha, fontsize=fs,
                              color=color, fontproperties=fp,
                              path_effects=_stroke, zorder=6)
            placed.append(_re.get_window_extent(renderer).expanded(1.12, 1.50))
        else:
            dropped += 1
    return dropped


def gen_galbraith(data, ax, theme, cjk_fp, **kwargs):
    """Galbraith 径向图（Meta 异质性可视化，漏斗图姊妹图；v5.6 第 36 号图型）。

    x=精度 1/SE，y=标准化效应 effect/SE；过原点固定效应回归线斜率 b=合并效应，
    ±1.96 平行带=同质区，带外研究=异质性/离群嫌疑（stderr 逐个报名+红圈高亮）。
    比率尺度（est_label=OR/HR/RR，效应取 log 值）默认画效应量弧线，把 y 轴读回
    临床尺度；MD/SMD 自动关弧线（差值尺度弧线无意义）。
    数据：与 funnel 完全同 schema；选项 est_label（默认 OR）/arcs（auto/true/false）。
    """
    names, es, ses = _meta_studies(data, "galbraith", hint="径向图分辨率有限")
    if len(es) < 3:
        raise ValueError("galbraith: 至少需要 3 个研究（精度-标准化效应平面才有可读性）")
    est_label = str(data.get("est_label") or "OR").upper()
    arcs_mode = data.get("arcs")
    if arcs_mode in (None, "auto"):
        arcs = est_label in _RATIO_LABELS
    else:
        if not isinstance(arcs_mode, bool):
            raise ValueError("galbraith: arcs 须为 true/false/auto")
        arcs = arcs_mode
        if arcs and est_label not in _RATIO_LABELS:
            _warn("galbraith: MD/SMD 等差值尺度的效应量弧线无意义，已自动关闭"
                  "（arcs 仅对比率尺度有意义）")
            arcs = False

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 2)
    c_main = theme["colors"][0]
    x = 1.0 / ses
    z = es / ses
    b = float(np.sum(x * z) / np.sum(x * x))   # 过原点加权回归=固定效应合并
    pooled = st.dl_pool(es, ses)               # stderr 报告 DL 随机效应口径

    x_hi = float(x.max()) * 1.08
    xg = np.linspace(0.0, x_hi, 64)
    ax.fill_between(xg, b * xg - 1.96, b * xg + 1.96,
                    color="#BBBBBB", alpha=0.18, zorder=1)
    for off in (-1.96, 1.96):
        ax.plot(xg, b * xg + off, color="#888888", lw=1.1, ls="--", zorder=2)
    ax.plot(xg, b * xg, color=c_main, lw=1.6, zorder=3,
            label=f"固定效应合并 b={b:.3g}")
    ax.axhline(0, color="#CCCCCC", lw=0.8, zorder=1)

    resid = z - b * x
    out_idx = [int(i) for i in np.where(np.abs(resid) > 1.96)[0]]
    ax.scatter(x, z, s=42, color=c_main, edgecolor="#333333",
               linewidth=0.8, zorder=4)
    for i in out_idx:   # 离群点红圈高亮（不遮数据点）
        ax.scatter([x[i]], [z[i]], s=130, facecolors="none",
                   edgecolors="#C0392B", linewidths=1.4, zorder=5)
    show_all = names and len(names) <= 12
    _x_right = float(x.max()) * 0.90   # 右缘标注左翻（端点 pad 铁律：右 10% 区域标签向左，防溢出画布）
    import matplotlib.patheffects as _pe
    _stroke = [_pe.withStroke(linewidth=2.2, foreground="white")]  # 白描边：标注压合并线仍可读（视觉验收结论落地）
    # v5.7：无效应参考线小标（比率尺度 y=0 即 OR=1；差值尺度=差值 0）
    _rl = f"{est_label}=1" if est_label in _RATIO_LABELS else "差值=0"
    ax.annotate(_rl, (x_hi, 0.0), ha="right", va="bottom", xytext=(0, 2),
                textcoords="offset points", fontsize=fs_s, color="#999999",
                path_effects=_stroke, zorder=2)
    _anns = []
    for i, nm in enumerate(names):
        if show_all or i in out_idx:
            _flip = x[i] >= _x_right
            _dx, _dy = (-7, 5) if _flip else (6, 5)
            _ha = "right" if _flip else "left"
            _color = "#8a1f1f" if i in out_idx else "#555555"
            _fp = cjk_fp if cjk_fp and _has_cjk(nm) else None
            _a = ax.annotate(nm, (x[i], z[i]), textcoords="offset points",
                             xytext=(_dx, _dy), ha=_ha, fontsize=fs_s,
                             color=_color, fontproperties=_fp,
                             path_effects=_stroke)
            _anns.append((_a, i in out_idx, nm, float(x[i]), float(z[i]),
                          (_dx, _dy), _ha, fs_s, _color, _fp))
    if names and len(names) > 12:
        _warn(f"galbraith: {len(names)} 个研究仅标离群名（>12 不逐个标注）"
              + ("" if out_idx else "，当前无离群"))

    ax.set_xlim(0, x_hi)
    pad = max(0.6, 0.08 * float(z.max() - z.min()))
    ax.set_ylim(min(float(z.min()), -2.2) - pad, max(float(z.max()), 2.2) + pad)
    _dropped = _declutter_annotations(ax, _anns)
    if _dropped:
        _warn(f"galbraith: {_dropped} 个研究名与相邻标注叠印已省略（数据点仍在图上）")
    if arcs:
        _pts = list(zip(x.tolist(), z.tolist()))
        _draw_galbraith_arcs(ax, b, x_hi, est_label, fs_s, cjk_fp, pts=_pts)
    xl = str(data.get("x_label") or "精度 1/SE")
    yl = (f"标准化效应（{est_label} 尺度）" if est_label in _RATIO_LABELS
          else "标准化效应 effect/SE")
    ax.set_xlabel(xl, fontproperties=cjk_fp if cjk_fp and _has_cjk(xl) else None)
    ax.set_ylabel(yl, fontproperties=cjk_fp if cjk_fp and _has_cjk(yl) else None)
    if ax.get_legend_handles_labels()[1]:
        ax.legend(fontsize=fs - 1, loc="upper left", framealpha=0.9, prop=cjk_fp)

    def _nm(i):
        return names[i] if i < len(names) and names[i] else f"研究{i+1}"
    _ol = "、".join(f"{_nm(i)}({resid[i]:+.2f})" for i in out_idx[:6])
    _warn(f"galbraith: 固定效应合并 b={b:.4g}；DL 随机效应 {pooled['pooled']:.4g}"
          f"（95%CI {pooled['pooled']-1.96*pooled['se']:.3g}~"
          f"{pooled['pooled']+1.96*pooled['se']:.3g}），I²={pooled['i2']:.0f}%，"
          f"P_het={pooled['p_het']:.3g}；"
          + (f"±1.96 带外离群 {len(out_idx)} 个：{_ol}" if out_idx
             else "研究均在 ±1.96 带内（未见明显异质性离群）"))
    if out_idx:
        _warn("galbraith: 带外研究是异质性主要来源——考虑随机效应合并（DL 已报）、"
              "分层 Meta 或剔除该研究的敏感性分析对照")
    return None


# ── cif 竞争风险累计发生率（v5.7 第 37 号图型；Aalen-Johansen） ────────

def _naive_one_minus_km(times, events, target=1):
    """1−KM 朴素估计（竞争事件当删失）——高估参照线。

    返回 (t_seq, one_minus_s_seq)，t 从 0 起（阶梯画法 where='post'）。"""
    e1 = [1 if int(e) == target else 0 for e in events]
    t_seq, s_seq, _ = st.km_estimate(times, e1)
    return t_seq, [1.0 - s for s in s_seq]


def gen_cif(data, ax, theme, cjk_fp, **kwargs):
    """竞争风险累计发生率图（Aalen-Johansen；v5.7 第 37 号图型）。

    有竞争事件（如死亡）时 1−KM 系统性高估目标事件的累计发生率（审稿高频
    退稿点）——实线按事件原因分解 AJ 累计发生率，compare_km 叠加 1−KM 朴素
    对照虚线直观显示高估幅度；stderr 报告事件计数/末点对比与口径提醒。
    数据：长表 time+event 两等长数组（0=删失 1=目标事件 ≥2=竞争事件编号），
    可选 cause_labels / percent / time_unit / y_max / compare_km（auto=有
    竞争事件才画）。多臂分组请用 -t km（v3.7 起内置 AJ 自动模式）。
    """
    t_raw = data.get("time")
    e_raw = data.get("event")
    if not isinstance(t_raw, list) or not isinstance(e_raw, list):
        if isinstance(data.get("groups"), dict):
            raise ValueError("cif: 不支持 groups 多臂分组——CIF 按事件原因分层；"
                             "多臂竞争风险请用 -t km（内置 AJ 自动模式）")
        raise ValueError("cif: 需要 'time'+'event' 两个等长数组"
                         "（0=删失 1=目标事件 ≥2=竞争事件）")
    if len(t_raw) != len(e_raw):
        raise ValueError(f"cif: time 有 {len(t_raw)} 个值但 event 有 "
                         f"{len(e_raw)} 个 — 长度必须一致")
    if not t_raw:
        raise ValueError("cif: 数据为空")
    try:
        times = [float(v) for v in t_raw]
    except (TypeError, ValueError):
        raise ValueError("cif: time 含非数值项（NaN/字符串）——请清洗后重试")
    try:
        events = [int(v) for v in e_raw]
    except (TypeError, ValueError):
        raise ValueError("cif: event 含非整数编码（须为 0=删失 1=目标事件 ≥2=竞争事件）")
    for _v, _e in zip(t_raw, e_raw):
        # v5.7 审计 P2：与 validate 层同口径——bool/字符串在 Python API 直调时也不静默放行
        if isinstance(_v, bool) or not isinstance(_v, (int, float)) or _v != _v:
            raise ValueError("cif: time 含非数值项（NaN/布尔/字符串）——请清洗后重试")
        if (isinstance(_e, bool) or not isinstance(_e, (int, float))
                or float(_e) != int(_e) or int(_e) < 0):
            raise ValueError(f"cif: event 编码须为 ≥0 整数（0=删失 1=目标事件 ≥2=竞争），"
                             f"发现 {_e!r}")
    if any(t < 0 for t in times):
        raise ValueError("cif: 存在负时间——随访时间须 ≥0")
    n = len(times)
    n1 = sum(1 for e in events if e == 1)
    comp_codes = sorted({e for e in events if e >= 2})
    nc = sum(1 for e in events if e == 0)
    if n1 == 0 and not comp_codes:
        raise ValueError("cif: 全部为删失（event 全 0）——无法估计累计发生率")

    cause_labels = data.get("cause_labels") if isinstance(data.get("cause_labels"), dict) else {}
    # ⛔键↔标签一致性守卫（10-24 全谱审计：ep35 标签对调同类——唯一的键间接映射点）
    _codes_in_data = {int(x) for x in e_raw if isinstance(x, (int, float)) and int(x) >= 1}
    for _k in cause_labels:
        try:
            _kc = int(_k)
        except (TypeError, ValueError):
            raise ValueError(f"cif: cause_labels 键「{_k}」不是整数事件码（合法：1=目标事件，≥2=竞争事件）")
        if _kc not in _codes_in_data:
            raise ValueError(f"cif: cause_labels 引用了数据中不存在的事件码 {_kc}"
                             f"（数据里实际出现的码：{sorted(_codes_in_data)}）——"
                             "八成是码与含义写反了，请核对 event 列编码")
    for _c in sorted(_codes_in_data):
        if _c >= 2 and str(_c) not in {str(k) for k in cause_labels}:
            print(f"cif: 竞争事件码 {_c} 未给 cause_labels，图例将用默认名「原因{_c}」", file=sys.stderr)
    compare_mode = data.get("compare_km", "auto")
    percent = bool(data.get("percent"))
    unit = str(data.get("time_unit") or "")

    aj = st.aalen_johansen(times, events)
    if compare_mode in (None, "auto"):
        compare = bool(comp_codes) and n1 > 0
    else:
        if not isinstance(compare_mode, bool):
            raise ValueError("cif: compare_km 须为 true/false/auto"
                             "（默认 auto=有竞争事件才画参照线）")
        compare = compare_mode and n1 > 0
        if compare_mode and not comp_codes:
            _warn("cif: 无竞争事件（无 ≥2 编码）——1−KM 与目标因累计发生率重合，"
                  "对照线已省略（此时 KM 口径正确，无需 CIF）")
            compare = False
        if compare_mode and n1 == 0:
            _warn("cif: 无目标事件（无 1 编码）——1−KM 对照线无对象，已省略")
            compare = False

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 2)
    _scale = 100.0 if percent else 1.0

    def _cause_name(j):
        v = cause_labels.get(str(j), cause_labels.get(j))
        return str(v) if v else ("目标事件" if j == 1 else f"竞争事件 {j}")

    for k, j in enumerate(sorted(aj["cif"].keys())):
        ys = [0.0] + [v * _scale for v in aj["cif"][j]]
        xs = [0.0] + list(aj["times"])
        ax.step(xs, ys, where="post", color=theme["colors"][k % len(theme["colors"])],
                lw=2, label=_cause_name(j), zorder=3)
    if compare:
        tk, sk = _naive_one_minus_km(times, events, 1)
        ax.step(tk, [v * _scale for v in sk], where="post", color="#888888",
                lw=1.4, ls="--", label="1−KM（竞争当删失，高估参照）", zorder=2)

    ax.set_xlabel(f"时间（{unit}）" if unit else "时间",
                  fontproperties=cjk_fp if cjk_fp and (_has_cjk(unit) or not unit) else None)
    yl = "累计发生率（%）" if percent else "累计发生率 Cumulative Incidence"
    ax.set_ylabel(yl, fontproperties=cjk_fp if cjk_fp and _has_cjk(yl) else None)
    _vals = [v * _scale for vs in aj["cif"].values() for v in vs]
    if compare and sk:
        _vals.append(max(sk) * _scale)
    _top = max(_vals + [0.0])
    import math as _m
    if percent:
        _top = max(10.0, _m.ceil(_top * 1.08 / 10.0) * 10.0)
    else:
        _top = max(0.10, _m.ceil(_top * 1.08 * 20.0) / 20.0)
    _user_top = data.get("y_max")
    if isinstance(_user_top, (int, float)) and _user_top > 0:
        ax.set_ylim(0, _user_top)
    else:
        ax.set_ylim(0, _top if percent else min(1.0, _top))
    if ax.get_legend_handles_labels()[1]:
        ax.legend(fontsize=fs - 1, loc="lower right", framealpha=0.9, prop=cjk_fp)

    def _end(states):
        out = {}
        for j in states:
            seq = aj["cif"].get(j)
            out[j] = seq[-1] if seq else 0.0
        return out

    _parts = "，".join(f"{_cause_name(j)} {_end([j])[j]:.3f}"
                       for j in sorted(aj["cif"].keys()))
    _tmax = aj["times"][-1] if len(aj["times"]) else 0.0
    _msg = (f"cif: n={n}（目标事件 {n1}"
            + (f"，竞争事件 {sum(1 for e in events if e >= 2)}" if comp_codes else "")
            + f"，删失 {nc}）；随访 0~{_tmax:g}" + unit)
    if aj["cif"]:
        _msg += f"；末点累计发生率——{_parts}"
    if compare:
        km_end = sk[-1] if sk else 0.0
        c1 = aj["cif"].get(1, [0.0])[-1]
        _msg += (f"；1−KM 末点 {km_end:.3f}（高估 "
                 f"{(km_end - c1) * 100:+.1f} 个百分点）")
        _warn("cif: 竞争风险下 1−KM 系统性高估目标事件累计发生率——"
              "论文请报告 CIF（Aalen-Johansen）口径并注明竞争事件")
    if n1 == 0:
        _warn("cif: 无目标事件（event=1）——仅绘制竞争事件累计发生率曲线")
    _warn(_msg)
    return None


# ── bland_altman 一致性分析 ───────────────────────────────────────────

def gen_bland_altman(data, ax, theme, cjk_fp, **kwargs):
    """Bland-Altman 一致性图：均值差 vs 均值，LoA=mean±1.96SD。

    数据: {"a": [...], "b": [...]} 或 {"methods": {"新方法": [...], "金标准": [...]}}
    （methods 恰好两项，差值=第一项−第二项）。
    """
    a, b, name_a, name_b = _two_series(data, "bland_altman")
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) != len(b) or len(a) < 3:
        raise ValueError(f"bland_altman: 两组数据须等长且 >=3 对（当前 {len(a)} vs {len(b)}）")
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("bland_altman: 含非数值/NaN")
    mean_ab = (a + b) / 2.0
    diff = a - b
    md = float(np.mean(diff))
    sd = float(np.std(diff, ddof=1))
    loa_hi, loa_lo = md + 1.96 * sd, md - 1.96 * sd

    ax.scatter(mean_ab, diff, s=34, color=theme["colors"][0],
               edgecolor="#333333", linewidth=0.8, zorder=4)
    ax.axhline(md, color=theme["colors"][1 % len(theme["colors"])], lw=1.4, zorder=3,
               label=f"均值差 {md:.3g}")
    for v, tag in ((loa_hi, "+1.96SD"), (loa_lo, "−1.96SD")):
        ax.axhline(v, color="#888888", lw=1.2, linestyle="--", zorder=3,
                   label=f"{tag} {v:.3g}")
    ax.axhline(0, color="#CCCCCC", lw=0.8, zorder=2)
    ax.set_xlabel(f"两法均值 ({name_a}/{name_b})")
    ax.set_ylabel(f"差值 ({name_a}−{name_b})")
    ax.legend(fontsize=theme["font_size"] - 1, loc="best", framealpha=0.9,
              prop=_fp(cjk_fp, name_a + name_b))
    _warn(f"bland_altman: 一致性界值 [{loa_lo:.3g}, {loa_hi:.3g}]，"
          f"差值均值 {md:.3g}（SD {sd:.3g}），n={len(a)}")
    return None


def _two_series(data, chart_name):
    """取恰好两个系列：支持 {'a':..,'b':..} 或 {'methods': {名:.., 名:..}}。"""
    if "a" in data and "b" in data:
        return data["a"], data["b"], str(data.get("label_a", "A")), str(data.get("label_b", "B"))
    methods = data.get("methods", None)
    if isinstance(methods, dict) and len(methods) == 2:
        (na, va), (nb, vb) = methods.items()
        return va, vb, str(na), str(nb)
    raise ValueError(
        f"{chart_name}: 需要 'a'+'b' 数组，或 'methods' 恰好两个系列 "
        f"（如 {{\"新方法\": [...], \"金标准\": [...]}}）")



def _declutter_texts(ax, texts, anchors, max_pass=120, step=9.0,
                     max_disp_frac=0.15, leader_min_frac=0.02):
    """散点数据标签防重叠：重叠排斥 + 锚点弹簧 + 位移上限 + 引导线。

    - 排斥：测量真实 bbox，重叠对互推（显示坐标测量、数据坐标移动）
    - 锚点弹簧：每轮向自己的数据点回拉，标签永不远离锚点
    - 位移上限：标签离锚点超过 max_disp_frac·min(轴跨度) 即强制拉回边界
    - 引导线：最终位移 > leader_min_frac 时画点→标签细线，保证对应关系可读
    返回剩余重叠对数。
    """
    if len(texts) < 2:
        return 0
    import math as _m
    fig = ax.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    span = min(x1 - x0, y1 - y0)
    max_disp = max_disp_frac * span
    leader_min = leader_min_frac * span
    for _pass in range(max_pass):
        bbs = [t.get_window_extent(renderer) for t in texts]
        n_over = 0
        moves = [(0.0, 0.0)] * len(texts)
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                bi, bj = bbs[i], bbs[j]
                if bi.x1 < bj.x0 or bj.x1 < bi.x0 or bi.y1 < bj.y0 or bj.y1 < bi.y0:
                    continue
                n_over += 1
                dx = (bi.x0 + bi.x1) / 2 - (bj.x0 + bj.x1) / 2
                dy = (bi.y0 + bi.y1) / 2 - (bj.y0 + bj.y1) / 2
                dist = _m.hypot(dx, dy) or 1.0
                ux, uy = dx / dist, dy / dist
                if abs(dx) < 0.5 and abs(dy) < 0.5:
                    ang = 2.399 * (i + 1)
                    ux, uy = _m.cos(ang), _m.sin(ang)
                moves[i] = (moves[i][0] + ux * step, moves[i][1] + uy * step)
                moves[j] = (moves[j][0] - ux * step, moves[j][1] - uy * step)
        if n_over == 0:
            break
        p0 = inv.transform((0, 0))
        p1 = inv.transform((step, step))
        ddx, ddy = p1[0] - p0[0], p1[1] - p0[1]
        for t, (mx, my), (axn, ayn) in zip(texts, moves, anchors):
            tx, ty = t.get_position()
            nx, ny = tx + mx * ddx, ty + my * ddy
            nx += (axn - nx) * 0.25   # 锚点弹簧
            ny += (ayn - ny) * 0.25
            ddx_a, ddy_a = nx - axn, ny - ayn
            dist_a = _m.hypot(ddx_a, ddy_a)
            if dist_a > max_disp:     # 位移上限：拉回锚点邻域
                nx = axn + ddx_a / dist_a * max_disp
                ny = ayn + ddy_a / dist_a * max_disp
            t.set_position((nx, ny))
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
    bbs = [t.get_window_extent(renderer) for t in texts]
    n_over = 0
    for i in range(len(bbs)):
        for j in range(i + 1, len(bbs)):
            if bbs[i].overlaps(bbs[j]):
                n_over += 1
    # 引导线：位移超阈值的标签画点→标签细线（对应关系可读）
    drawn = 0
    for t, (axn, ayn) in zip(texts, anchors):
        tx, ty = t.get_position()
        if _m.hypot(tx - axn, ty - ayn) > leader_min:
            ax.plot([axn, tx], [ayn, ty], color="#AAAAAA", linewidth=0.7,
                    zorder=5, clip_on=False)
            drawn += 1
    return n_over


def _thin_overlapping_texts(ax, texts):
    """最后手段：反复移除卷入重叠最多的标签，直到无重叠。返回移除数（调用方发 stderr 警告）。"""
    fig = ax.figure
    removed = 0
    while texts:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bbs = [t.get_window_extent(renderer) for t in texts]
        worst, worst_n = -1, 0
        for i, bi in enumerate(bbs):
            n = sum(1 for j, bj in enumerate(bbs) if j != i and bi.overlaps(bj))
            if n > worst_n:
                worst, worst_n = i, n
        if worst_n == 0:
            break
        texts[worst].remove()
        texts.pop(worst)
        removed += 1
    return removed


# ── pca 得分图 ────────────────────────────────────────────────────────

def gen_pca(data, ax, theme, cjk_fp, **kwargs):
    """PCA 得分图（PC1×PC2）：标准化默认开，分组椭圆=均值±2SD，载荷 top5。

    数据: {"matrix": [[...]], "row_labels": [...], "groups": [...](可选, 按行),
           "feature_names": [...]}
    """
    matrix = data.get("matrix", data.get("values", None))
    if matrix is None or not isinstance(matrix, (list, tuple)) or len(matrix) == 0:
        raise ValueError("pca: 需要 'matrix'（二维数值数组，行=样本 列=特征）")
    X = np.asarray(matrix, dtype=float)
    if X.ndim != 2 or X.shape[0] < 3:
        raise ValueError(f"pca: 矩阵需 >=3 行样本（当前 {X.shape}）")
    if X.shape[1] < 2:
        raise ValueError("pca: 至少 2 个特征列")
    if X.shape[1] > MAX_PCA_COLS:
        raise ValueError(f"pca: 特征列 {X.shape[1]} 超过上限 {MAX_PCA_COLS}（维度过高请先降维/筛选）")
    if np.any(~np.isfinite(X)):
        raise ValueError("pca: 矩阵含 NaN/Inf——请先补全或剔除")
    row_labels = list(data.get("row_labels", data.get("labels", [])))
    groups = data.get("groups", None)
    feature_names = list(data.get("feature_names", [f"特征{i+1}" for i in range(X.shape[1])]))
    if len(feature_names) != X.shape[1]:
        print(f"WARNING: pca feature_names 数量（{len(feature_names)}）与变量数"
              f"（{X.shape[1]}）不符，已自动改用默认名 特征1..{X.shape[1]}", file=sys.stderr)
        feature_names = [f"特征{i+1}" for i in range(X.shape[1])]

    scale = kwargs.get("scale", True)
    Xc = X - X.mean(axis=0)
    if scale:
        sd = X.std(axis=0, ddof=1)
        if np.any(sd == 0):
            zero_cols = int(np.sum(sd == 0))
            keep = sd > 0
            Xc = Xc[:, keep]
            feature_names = [f for f, k in zip(feature_names, keep) if k]
            _warn(f"pca: {zero_cols} 个零方差特征列已剔除")
            if Xc.shape[1] < 2:
                raise ValueError("pca: 剔除零方差列后不足 2 列")
        Xc = Xc / Xc.std(axis=0, ddof=1)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    scores = U * S
    total_var = float(np.sum(S ** 2))
    var_pct = [S[i] ** 2 / total_var * 100 for i in range(min(2, len(S)))]

    import math as _m
    label_texts = []
    _anchors = []
    if groups and isinstance(groups, (list, tuple)) and len(groups) == X.shape[0]:
        uniq = list(dict.fromkeys(str(g) for g in groups))
        for gi, g in enumerate(uniq):
            mask = np.array([str(x) == g for x in groups])
            pts = scores[mask, :2]
            c = theme["colors"][gi % len(theme["colors"])]
            ax.scatter(pts[:, 0], pts[:, 1], s=36, color=c, edgecolor="#333333",
                       linewidth=0.8, zorder=4, label=str(g))
            if mask.sum() >= 3:
                mu = pts.mean(axis=0)
                sd_pts = pts.std(axis=0, ddof=1)
                theta = np.linspace(0, 2 * np.pi, 72)
                ell = np.c_[mu[0] + 2 * sd_pts[0] * np.cos(theta),
                            mu[1] + 2 * sd_pts[1] * np.sin(theta)]
                ax.plot(ell[:, 0], ell[:, 1], color=c, linewidth=1.1,
                        alpha=0.65, linestyle="--", zorder=3)
    else:
        ax.scatter(scores[:, 0], scores[:, 1], s=36, color=theme["colors"][0],
                   edgecolor="#333333", linewidth=0.8, zorder=4)
        if 0 < len(row_labels) == X.shape[0] and X.shape[0] <= 40:
            _fs = max(6, theme["font_size"] - 2)
            _sx = float(np.ptp(scores[:, 0])) or 1.0
            _sy = float(np.ptp(scores[:, 1])) or 1.0
            _anchors = []
            for i, rl in enumerate(row_labels):
                ang = 2.399 * i  # 黄金角环绕初始位，天然散开减少推移
                ox, oy = _sx * 0.02 * _m.cos(ang), _sy * 0.02 * _m.sin(ang)
                label_texts.append(ax.text(
                    scores[i, 0] + ox, scores[i, 1] + oy,
                    str(rl), fontsize=_fs, color="#555555",
                    fontproperties=_fp(cjk_fp, rl), zorder=6,
                    ha="center", va="center"))
                _anchors.append((scores[i, 0], scores[i, 1]))

    # 载荷箭头 top5（|PC1|+|PC2|）
    loadings = Vt[:2, :].T
    imp = np.abs(loadings).sum(axis=1)
    top_idx = np.argsort(imp)[::-1][:5]
    scale_l = np.abs(scores[:, :2]).max() * 0.42 / max(imp[top_idx].max(), 1e-12)
    import matplotlib.patches as _mpatches
    _sx = float(np.ptp(scores[:, 0])) or 1.0
    _sy = float(np.ptp(scores[:, 1])) or 1.0
    _ac = theme["colors"][-1]  # v7.9.1 AF33：载荷箭头色入主题（原硬编码琥珀不随 --theme）
    for idx in top_idx:
        lx, ly = loadings[idx, 0] * scale_l, loadings[idx, 1] * scale_l
        ax.add_patch(_mpatches.FancyArrowPatch(
            (0, 0), (lx, ly), arrowstyle="->", mutation_scale=14,
            color=_ac, lw=1.3, zorder=5, shrinkA=0, shrinkB=0))
        label_texts.append(ax.text(
            lx + _sx * 0.012, ly + _sy * 0.012, feature_names[idx],
            fontsize=max(6, theme["font_size"] - 2), color=_ac,
            fontproperties=_fp(cjk_fp, feature_names[idx]), zorder=7,
            ha="left", va="bottom"))
        _anchors.append((lx, ly))
    ax.axhline(0, color="#CCCCCC", lw=0.8, zorder=1)
    ax.axvline(0, color="#CCCCCC", lw=0.8, zorder=1)
    ax.set_xlabel(f"PC1（解释 {var_pct[0]:.1f}%）")
    ax.set_ylabel(f"PC2（解释 {var_pct[1]:.1f}%）")
    if groups:
        ax.legend(fontsize=theme["font_size"] - 1, loc="best", framealpha=0.9,
                  prop=_fp(cjk_fp, " ".join(str(g) for g in groups)))
    ax.update_datalim(scores[:, :2])
    ax.autoscale_view()
    if label_texts:
        n_left = _declutter_texts(ax, label_texts, _anchors)
        if n_left > 0:
            removed = _thin_overlapping_texts(ax, label_texts)
            if removed:
                _warn(f"pca: 样本标签过密，已省略 {removed} 个重叠标签"
                      "（完整样本清单见 --alt 无障碍描述）")
    _warn(f"pca: PC1+PC2 累计解释 {var_pct[0]+var_pct[1]:.1f}% 方差"
          f"（标准化={'是' if scale else '否'}）")
    return None


# ── paired 配对前后图 ─────────────────────────────────────────────────

def gen_paired(data, ax, theme, cjk_fp, **kwargs):
    """配对前后折线图：每个受试对象一条线 + 配对检验（配对 t / Wilcoxon 符号秩）。

    数据: {"before": [...], "after": [...]} 或
          {"series": {"术前": [...], "术后": [...]}}（恰好两项）+ 可选 labels。
    """
    from scipy import stats as _st
    if "before" in data and "after" in data:
        a = list(data["before"]); b = list(data["after"])
        name_a, name_b = str(data.get("label_a", "Before")), str(data.get("label_b", "After"))
    else:
        series = data.get("series", None)
        if not (isinstance(series, dict) and len(series) == 2):
            raise ValueError(
                "paired: 需要 'before'+'after' 数组，或 'series' 恰好两项"
                "（如 {\"术前\": [...], \"术后\": [...]}）")
        (name_a, a), (name_b, b) = series.items()
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) != len(b) or len(a) < 2:
        raise ValueError(f"paired: 两组须等长且 >=2 对（当前 {len(a)} vs {len(b)}）")
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("paired: 含非数值/NaN")

    n = len(a)
    c_a = theme["colors"][0]; c_b = theme["colors"][1 % len(theme["colors"])]
    for i in range(n):
        ax.plot([0, 1], [a[i], b[i]], color="#B9B9B9", lw=1.1, zorder=2,
                marker="o", markersize=4, markerfacecolor="white",
                markeredgecolor="#777777")
    ax.scatter(np.zeros(n), a, s=42, color=c_a, edgecolor="#333333",
               linewidth=0.8, zorder=4, label=name_a)
    ax.scatter(np.ones(n), b, s=42, color=c_b, edgecolor="#333333",
               linewidth=0.8, zorder=4, label=name_b)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([name_a, name_b],
                       fontproperties=_fp(cjk_fp, name_a + name_b))
    ax.set_xlim(-0.35, 1.35)

    if kwargs.get("stats_auto"):
        d = b - a
        use_t = True
        if 3 <= n <= 5000 and float(_st.shapiro(d).pvalue) <= 0.05:
            use_t = False
        if n >= 6 and use_t:
            _, p = _st.ttest_rel(b, a)
            method = "配对 t 检验"
        elif n >= 6:
            _, p = _st.wilcoxon(b, a)
            method = "Wilcoxon 符号秩"
        else:
            _warn(f"paired: n={n} <6，检验效力不足，未做统计标注")
            p, method = None, ""
        if p is not None:
            stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "n.s."
            top = float(max(a.max(), b.max()))
            span = max(abs(top) * 0.08, 1e-9)
            yi = top + span
            ax.plot([0, 0, 1, 1], [yi - span * 0.25, yi, yi, yi - span * 0.25],
                    color="#333333", lw=1.2, zorder=6)
            ax.text(0.5, yi + span * 0.08, stars, ha="center", va="bottom",
                    fontsize=max(7, theme["font_size"]), color="#333333", zorder=6)
            ax.set_ylim(top=yi + span * 0.7)
            _warn(f"paired: {name_b} vs {name_a}：{method}，p={p:.4g} → {stars}")
    ax.set_ylabel("测量值")
    ax.legend(fontsize=theme["font_size"] - 1, loc="best", framealpha=0.9,
              prop=_fp(cjk_fp, name_a + name_b))
    return None


# ── venn 韦恩图 ───────────────────────────────────────────────────────

# ── venn 面积比例（Euler）几何求解 ────────────────────────────────────

def _circle_overlap_area(d, r1, r2):
    """两圆交集面积（d=圆心距）。d>=r1+r2 → 0；d<=|r1-r2| → 较小圆全面积。"""
    import math as _m
    if d >= r1 + r2:
        return 0.0
    r_min = min(r1, r2)
    if d <= abs(r1 - r2):
        return _m.pi * r_min * r_min
    a1 = r1 * r1 * _m.acos((d * d + r1 * r1 - r2 * r2) / (2 * d * r1))
    a2 = r2 * r2 * _m.acos((d * d + r2 * r2 - r1 * r1) / (2 * d * r2))
    a3 = 0.5 * _m.sqrt(max(0.0, (-d + r1 + r2) * (d + r1 - r2)
                                * (d - r1 + r2) * (d + r1 + r2)))
    return a1 + a2 - a3


_R_MIN = 0.04  # 空集/极小集合仍可辨识的最小视觉半径（0-1 归一坐标）


def _fit_into_unit(centers, radii, margin=0.16):
    """把布局（任意单位）平移缩放到 [0,1]² 内切（留 margin 给集合名标签）。
    返回 (centers, radii, affine)，affine=(cx, cy, s) 供质心同批换算。"""
    xs = [c[0] for c in centers]
    ys = [c[1] for c in centers]
    x0, x1 = min(xs) - max(radii), max(xs) + max(radii)
    y0, y1 = min(ys) - max(radii), max(ys) + max(radii)
    span = max(x1 - x0, y1 - y0) or 1.0
    s = (1.0 - 2 * margin) / span
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    out_c = [((c[0] - cx) * s + 0.5, (c[1] - cy) * s + 0.5) for c in centers]
    return out_c, [r * s for r in radii], (cx, cy, s)


def _venn2_geometry(n1, n2, inter):
    """2 集合 Euler 布局（解析解）。n1=|A\\B|, n2=|B\\A|, inter=|A∩B|（计数）。

    返回 (centers, radii, notes)：notes 为需 stderr 提示的异常布局说明列表。"""
    import math as _m
    from scipy.optimize import brentq
    t1, t2 = n1 + inter, n2 + inter
    if inter > t1 or inter > t2:
        raise ValueError("venn --area: 区域计数不自洽——交集计数不能大于任一集合的总数"
                         f"（当前交={inter}，两集合总={t1}/{t2}）")
    notes = []
    if t1 <= 0 and t2 <= 0:
        return [(0.40, 0.50), (0.60, 0.50)], [_R_MIN, _R_MIN], ["两个集合均为空"]
    r1 = _m.sqrt(t1 / _m.pi) if t1 > 0 else None
    r2 = _m.sqrt(t2 / _m.pi) if t2 > 0 else None
    if inter <= 0:
        # 不相交（或单侧为空）：留 12% 间隙并列
        if t1 <= 0:
            notes.append("集合 A 为空（图中以最小圆示意）")
        if t2 <= 0:
            notes.append("集合 B 为空（图中以最小圆示意）")
        rr1 = max(r1 if t1 > 0 else 0.0, 0.0)
        rr2 = max(r2 if t2 > 0 else 0.0, 0.0)
        d = (rr1 + rr2) * 1.12
        centers, radii, _aff = _fit_into_unit([(-d / 2, 0.0), (d / 2, 0.0)], [rr1, rr2])
        return centers, radii, notes
    if n1 <= 0 and n2 <= 0:
        # 两集合完全相同：同心微偏，仍能看出两层边
        r = _m.sqrt(t1 / _m.pi)
        centers, radii, _aff = _fit_into_unit([(0.0, 0.0), (0.0, 0.0)], [r, r])
        radii[1] = radii[0] * 0.985
        notes.append("两集合元素完全相同（同心绘制）")
        return centers, radii, notes
    if n1 <= 0 or n2 <= 0:
        # 单侧包含：A ⊆ B（或反向），内切
        if n1 <= 0:
            r_in, r_out = r1, r2
        else:
            r_in, r_out = r2, r1
        d = r_out - r_in
        centers, radii, _aff = _fit_into_unit([(0.0, 0.0), (d, 0.0)], [r_out, r_in])
        if n1 <= 0:
            centers = centers[::-1]
            radii = radii[::-1]
        notes.append("子集关系：小集合完全包含于大集合")
        return centers, radii, notes
    # 常规：半径固定，brentq 解圆心距 d 使交集面积=inter（面积单位=计数）
    lo, hi = abs(r1 - r2) * (1 + 1e-9), (r1 + r2) * (1 - 1e-9)
    f = lambda d: _circle_overlap_area(d, r1, r2) - inter
    if f(lo) < 0:      # inter 达到包含上限（计数不自洽的边界）
        d = lo
    elif f(hi) > 0:    # inter 小于相切下限（几乎不相交）
        d = hi
    else:
        d = brentq(f, lo, hi, xtol=1e-10, rtol=1e-12)
    centers, radii, _aff = _fit_into_unit([(0.0, 0.0), (d, 0.0)], [r1, r2])
    return centers, radii, notes


def _venn_region_masks(centers, radii, box, res):
    """网格化各区域（2 或 3 圆），返回 (area dict, centroid dict, cell_area)。
    box=(x0,y0,x1,y1)；area 以坐标面积为单位；centroid 为数据坐标（空区域为 None）。
    键：单集 "1"/"2"[/"3"]、两两 "12"…、三集 "123"。"""
    xs = np.linspace(box[0], box[2], res)
    ys = np.linspace(box[1], box[3], res)
    X, Y = np.meshgrid(xs, ys)
    cell = (box[2] - box[0]) * (box[3] - box[1]) / (res * res)
    ins = [(X - c[0]) ** 2 + (Y - c[1]) ** 2 <= r * r for c, r in zip(centers, radii)]
    if len(ins) == 2:
        a, b = ins
        masks = {"1": a & ~b, "2": b & ~a, "12": a & b}
    else:
        a, b, c = ins
        masks = {"1": a & ~b & ~c, "2": b & ~a & ~c, "3": c & ~a & ~b,
                 "12": a & b & ~c, "13": a & c & ~b, "23": b & c & ~a,
                 "123": a & b & c}
    areas, cents = {}, {}
    for k, m in masks.items():
        n = int(m.sum())
        areas[k] = n * cell
        cents[k] = (float(X[m].mean()), float(Y[m].mean())) if n else None
    return areas, cents, cell


def _triple_overlap_area(c1, c2, c3, r1, r2, r3, n=2048):
    """三圆交集面积：竖弦长 1D 积分（凸集 → 截面交集=交集截面，无网格噪声）。
    L(x) = max(0, min(上弦) − max(下弦))，逐圆弦在圆外时长度取 0。"""
    cxs = (c1[0], c2[0], c3[0])
    cys = (c1[1], c2[1], c3[1])
    rs = (r1, r2, r3)
    x0 = max(cx - r for cx, r in zip(cxs, rs))
    x1 = min(cx + r for cx, r in zip(cxs, rs))
    if x1 <= x0:
        return 0.0
    xs = np.linspace(x0, x1, n)
    los, his = [], []
    for cx, cy, r in zip(cxs, cys, rs):
        dx2 = np.clip(r * r - (xs - cx) ** 2, 0.0, None)
        s = np.sqrt(dx2)
        los.append(cy - s)
        his.append(cy + s)
    lower = np.maximum.reduce(los)
    upper = np.minimum.reduce(his)
    L = np.clip(upper - lower, 0.0, None)
    return float(np.sum((L[1:] + L[:-1]) * 0.5 * np.diff(xs)))


def _venn3_geometry(regions, keys):
    """3 集合 Euler 布局：半径由集合总数定，圆心按区域计数拟合。

    目标函数 6/7 项解析（成对交集闭式解 + 容斥单集），仅三集合项用小网格，
    避免纯网格分段常数导致的 trust-region 早停；初值=成对解析解三角布置。
    regions 键：k1/k2/k3/k1k2/k1k3/k2k3/k1k2k3（计数）。
    返回 (centers, radii, fit)；fit 含 max_rel_err（非零区域最大面积相对偏差）。
    """
    import math as _m
    from scipy.optimize import least_squares, brentq
    k1, k2, k3 = keys
    idx = {k1: "1", k2: "2", k3: "3", k1 + k2: "12", k1 + k3: "13",
           k2 + k3: "23", k1 + k2 + k3: "123"}
    target = {v: float(regions[k]) for k, v in idx.items()}
    totals = [target["1"] + target["12"] + target["13"] + target["123"],
              target["2"] + target["12"] + target["23"] + target["123"],
              target["3"] + target["13"] + target["23"] + target["123"]]
    radii_ideal = [_m.sqrt(t / _m.pi) if t > 0 else 1e-3 for t in totals]

    def _pair_d(i, j, ov):
        """解析解两圆心距使交集面积=ov；不可行时夹到边界。"""
        ri, rj = radii_ideal[i], radii_ideal[j]
        lo, hi = abs(ri - rj) * (1 + 1e-9), (ri + rj) * (1 - 1e-9)
        f = lambda d: _circle_overlap_area(d, ri, rj) - ov
        if ov <= 0:
            return hi + (ri + rj) * 0.12
        if f(lo) < 0:
            return lo
        if f(hi) > 0:
            return hi
        return brentq(f, lo, hi, xtol=1e-10, rtol=1e-12)

    # 初值：成对交集 = 两两区域 + 三集合，解析求三个圆心距 → 三角布置
    d12 = _pair_d(0, 1, target["12"] + target["123"])
    d13 = _pair_d(0, 2, target["13"] + target["123"])
    d23 = _pair_d(1, 2, target["23"] + target["123"])

    def regions_from_centers(centers, radii):
        c1, c2, c3 = centers
        ov12 = _circle_overlap_area(_m.hypot(c1[0] - c2[0], c1[1] - c2[1]),
                                    radii[0], radii[1])
        ov13 = _circle_overlap_area(_m.hypot(c1[0] - c3[0], c1[1] - c3[1]),
                                    radii[0], radii[2])
        ov23 = _circle_overlap_area(_m.hypot(c2[0] - c3[0], c2[1] - c3[1]),
                                    radii[1], radii[2])
        tri = _triple_overlap_area(c1, c2, c3, radii[0], radii[1], radii[2])
        only1 = _m.pi * radii[0] ** 2 - ov12 - ov13 + tri
        only2 = _m.pi * radii[1] ** 2 - ov12 - ov23 + tri
        only3 = _m.pi * radii[2] ** 2 - ov13 - ov23 + tri
        return [only1, only2, only3, ov12 - tri, ov13 - tri, ov23 - tri, tri]

    # 圆心 + 半径联合拟合（venneuler 思路）：固定半径的圆无法精确实现任意
    # 7 区域面积（数学上常无解），放开半径 + 锚定惩罚项可把误差压到低个位数 %
    _rad_w = 0.35

    def residuals(p):
        centers = [(p[0], p[1]), (p[2], p[3]), (p[4], p[5])]
        radii = [p[6], p[7], p[8]]
        got = regions_from_centers(centers, radii)
        res = [(g - t) / max(t, 1.0)
               for g, t in zip(got, target.values())]
        res += [_rad_w * (r - ri) / ri
                for r, ri in zip(radii, radii_ideal)]
        return res

    # 多起点（成对解析三角布置 / 嵌套堆叠 / 等边对称），各自两段精修，取代价最小者
    r_max0 = max(radii_ideal)
    cos_a = (d12 * d12 + d13 * d13 - d23 * d23) / (2 * d12 * d13)
    cos_a = max(-1.0, min(1.0, cos_a))
    tri_pt = (d13 * cos_a, d13 * _m.sqrt(max(0.0, 1.0 - cos_a * cos_a)))
    inits = [
        np.array([0.0, 0.0, d12, 0.0, tri_pt[0], tri_pt[1], *radii_ideal]),
        np.array([0.0, 0.0, 0.25 * radii_ideal[0], 0.0,
                  0.1 * radii_ideal[0], 0.2 * radii_ideal[1], *radii_ideal]),
        np.array([-1.1 * r_max0, 0.6 * r_max0, 1.1 * r_max0, 0.6 * r_max0,
                  0.0, -0.8 * r_max0, *radii_ideal]),
    ]
    lo = np.array([-np.inf] * 6 + [0.02 * r for r in radii_ideal])
    best = None
    for x0 in inits:
        sol = least_squares(residuals, x0, bounds=(lo, np.inf), diff_step=1e-3,
                            xtol=1e-14, ftol=1e-14, max_nfev=1200)
        sol = least_squares(residuals, sol.x, bounds=(lo, np.inf), diff_step=1e-4,
                            xtol=1e-15, ftol=1e-15, max_nfev=1200)
        if best is None or sol.cost < best.cost:
            best = sol
    sol = best
    centers = [(sol.x[0], sol.x[1]), (sol.x[2], sol.x[3]), (sol.x[4], sol.x[5])]
    radii = [float(sol.x[6]), float(sol.x[7]), float(sol.x[8])]
    # 精细网格硬面积复算（报告 + 质心），与目标函数解耦
    all_r = max(radii)
    xs = [c[0] for c in centers]
    ys = [c[1] for c in centers]
    box = (min(xs) - all_r - 1.0, min(ys) - all_r - 1.0,
           max(xs) + all_r + 1.0, max(ys) + all_r + 1.0)
    areas, cents, _cell = _venn_region_masks(centers, radii, box, 500)
    nz = [abs(areas[k] - target[k]) / target[k] for k in target if target[k] > 0]
    max_rel = max(nz) if nz else 0.0
    centers_u, radii_u, (cx, cy, s) = _fit_into_unit(centers, radii)
    cents_u = {k: (None if v is None else ((v[0] - cx) * s + 0.5, (v[1] - cy) * s + 0.5))
               for k, v in cents.items()}
    fit = {"max_rel_err": max_rel, "centroids": cents_u}
    return centers_u, radii_u, fit


# ── v2.8 D1：venn 4 集合（椭圆风车布局）──────────────────────────────────
_V4_R, _V4_A, _V4_B = 0.10, 0.32, 0.20  # 布局常数：网格探针验证 15 区域全非空


def _venn4_ells(r=_V4_R, a=_V4_A, b=_V4_B):
    """默认 4 椭圆布局（径向风车式，坐标中心为原点）：[(cx,cy,a,b,θrad)×4]。"""
    import math as _m
    return [(r * _m.cos(_m.pi / 2 + i * _m.pi / 2),
             r * _m.sin(_m.pi / 2 + i * _m.pi / 2), a, b,
             _m.pi / 2 + i * _m.pi / 2) for i in range(4)]


def _venn4_region_masks(ells, box, res):
    """网格化 4 椭圆的 15 个区域（确定性，无随机）。ells=[(cx,cy,a,b,θ)]，
    返回 (areas, centroids, cell_area)，键为成员并排序号 "1".."4"/"12"/"1234"；
    空区域 centroids=None。"""
    import itertools as _it
    xs = np.linspace(box[0], box[2], res)
    ys = np.linspace(box[1], box[3], res)
    X, Y = np.meshgrid(xs, ys)
    cell = (box[2] - box[0]) * (box[3] - box[1]) / (res * res)
    ins = []
    for (cx, cy, a, b, th) in ells:
        ct, st = np.cos(th), np.sin(th)
        dx, dy = X - cx, Y - cy
        u = dx * ct + dy * st
        v = -dx * st + dy * ct
        ins.append((u * u) / (a * a) + (v * v) / (b * b) <= 1.0)
    areas, cents = {}, {}
    for n in (1, 2, 3, 4):
        for combo in _it.combinations(range(4), n):
            m = np.ones_like(X, dtype=bool)
            for i in range(4):
                m = m & (ins[i] if i in combo else ~ins[i])
            key = "".join(str(i + 1) for i in combo)
            cnt = int(m.sum())
            areas[key] = cnt * cell
            cents[key] = (float(X[m].mean()), float(Y[m].mean())) if cnt else None
    return areas, cents, cell


def _venn4_geometry(regions, keys):
    """4 集合 --area：椭圆联合最优拟合（eulerAPE 思路，零新依赖）。

    (cx,cy,a,b,θ)×4 最小二乘，残差=15 区域网格面积 vs 目标比例；低分辨率网格
    定向 + 高分辨率复核（全程确定性）。任意 15 区域面积组合在椭圆几何下可能
    无解——非零区域最大面积相对偏差如实写入 fit["max_rel_err"] 由调用方披露。
    返回 (ells_unit, fit)；ells_unit 已归一到 [0,1]²，fit["centroids"] 同坐标系。"""
    import itertools as _it
    import math as _m
    from scipy.optimize import least_squares
    idx = {}
    for n in (1, 2, 3, 4):
        for combo in _it.combinations(range(4), n):
            idx["".join(keys[i] for i in combo)] = "".join(str(i + 1) for i in combo)
    target = {mk: float(regions[nk]) for nk, mk in idx.items()}
    tsum = sum(target.values()) or 1.0

    def residuals(p, res):
        ells = [(p[5 * i], p[5 * i + 1], abs(p[5 * i + 2]), abs(p[5 * i + 3]),
                 p[5 * i + 4]) for i in range(4)]
        got, _ce, _cl = _venn4_region_masks(ells, (-0.6, -0.6, 0.6, 0.6), res)
        gsum = sum(got.values()) or 1.0
        s = tsum / gsum
        out = []
        for mk in sorted(target):
            t = target[mk]
            if t > 0:
                out.append((got[mk] * s - t) / max(t, 1.0))
            else:
                out.append(0.3 * min(got[mk] * s, 1.0))  # 零目标区域温和压空
        return out

    lo, hi = [], []
    for _ in range(4):
        lo += [-0.6, -0.6, 0.05, 0.04, -2 * _m.pi]
        hi += [0.6, 0.6, 0.85, 0.85, 2 * _m.pi]
    lo, hi = np.array(lo), np.array(hi)
    x0 = []
    for (cx, cy, a, b, th) in _venn4_ells():
        x0 += [cx, cy, a, b, th]
    x0 = np.array(x0)
    scale0 = np.array([1, 1, 0.8, 0.8, 1] * 4)
    best = None
    for s0 in (x0, x0 * scale0, np.clip(x0 * 1.1, lo, hi)):
        sol = least_squares(residuals, np.clip(s0, lo, hi), bounds=(lo, hi),
                            args=(200,), diff_step=1e-2, xtol=1e-10, ftol=1e-10,
                            max_nfev=400)
        sol = least_squares(residuals, sol.x, bounds=(lo, hi), args=(320,),
                            diff_step=3e-3, xtol=1e-12, ftol=1e-12, max_nfev=500)
        if best is None or sol.cost < best.cost:
            best = sol
    p = best.x
    ells = [(p[5 * i], p[5 * i + 1], abs(p[5 * i + 2]), abs(p[5 * i + 3]),
             p[5 * i + 4]) for i in range(4)]
    E = max(max(abs(e[0]) + e[2], abs(e[1]) + e[2]) for e in ells) or 1.0
    s = 0.42 / E
    ells_u = [(e[0] * s + 0.5, e[1] * s + 0.5, e[2] * s, e[3] * s, e[4])
              for e in ells]
    areas, cents, _c = _venn4_region_masks(ells_u, (0.0, 0.0, 1.0, 1.0), 620)
    gsum = sum(areas.values()) or 1.0
    s2 = tsum / gsum
    nz = [abs(areas[mk] * s2 - t) / t for mk, t in target.items() if t > 0]
    fit = {"max_rel_err": (max(nz) if nz else 0.0), "centroids": cents}
    return ells_u, fit


def _declutter_points(points, min_dist=0.078, iters=48, relax=0.6):
    """确定性标签疏散：对过近标签对做对称排斥迭代（无随机，同输入同结果）。
    points: {key: (x, y)}；返回新 dict（仅移动过近者，其余原位）。"""
    pts = {k: [float(v[0]), float(v[1])] for k, v in sorted(points.items())
           if v is not None}
    keys = sorted(pts)
    for _ in range(iters):
        moved = False
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = pts[keys[i]], pts[keys[j]]
                dx, dy = b[0] - a[0], b[1] - a[1]
                dist = (dx * dx + dy * dy) ** 0.5
                if dist >= min_dist:
                    continue
                if dist < 1e-9:
                    dx, dy, dist = 1.0, 0.0, 1.0
                push = (min_dist - dist) * relax / 2.0
                ux, uy = dx / dist, dy / dist
                pts[keys[i]][0] -= ux * push
                pts[keys[i]][1] -= uy * push
                pts[keys[j]][0] += ux * push
                pts[keys[j]][1] += uy * push
                moved = True
        if not moved:
            break
    return {k: tuple(v) for k, v in pts.items()}


def _gen_venn4(ax, keys, regions, colors, fs, cjk_fp, area_mode):
    """v2.8 D1：4 集合韦恩绘制（椭圆）。默认=固定风车布局、15 区域计数全标；
    area_mode=按面积比例最优拟合（残差中文披露，数字仍为精确计数）。"""
    import itertools as _it
    import math as _m
    import matplotlib.patches as mpatches
    if area_mode:
        ells, fit = _venn4_geometry(regions, keys)
        _ar, cents, _c = _venn4_region_masks(ells, (0.0, 0.0, 1.0, 1.0), 620)
        max_rel = fit["max_rel_err"]
        if max_rel <= 0.05:
            print(f"venn --area: 4 集合椭圆拟合完成"
                  f"（最大区域面积偏差 {max_rel * 100:.1f}%）", file=sys.stderr)
        else:
            _warn(f"venn --area: 15 个区域面积在椭圆几何下无法完全按比例实现，"
                  f"已取最优拟合（最大面积偏差 {max_rel * 100:.1f}%）；"
                  f"区域数字仍为精确计数")
            if max_rel > 0.15:
                _warn("venn --area: 偏差较大——可尝试 ①减少集合数（2~3 集合拟合更准）"
                      "②去掉占比悬殊的区域 ③改用默认等圆模式（放弃面积比例）")
    else:
        ells = [(cx + 0.5, cy + 0.5, a, b, th)
                for (cx, cy, a, b, th) in _venn4_ells()]
        _ar, cents, _c = _venn4_region_masks(ells, (0.0, 0.0, 1.0, 1.0), 420)

    for i in range(4):
        cx, cy, a, b, th = ells[i]
        ax.add_patch(mpatches.Ellipse(
            (cx, cy), 2 * a, 2 * b, angle=_m.degrees(th),
            facecolor=colors[i % len(colors)], edgecolor="#333333",
            linewidth=1.4, alpha=0.42, zorder=2))

    zero_regions = []
    label_plan = []  # (mkey, cnt, pos)：先收集，疏散后统一画（中心 5 区域质心彼此很近）
    for n in (1, 2, 3, 4):
        for combo in _it.combinations(range(4), n):
            mkey = "".join(str(i + 1) for i in combo)
            rname = "".join(keys[i] for i in combo)
            cnt = regions[rname]
            pos = cents.get(mkey)
            if pos is None:
                if cnt > 0:
                    _warn(f"venn: 区域 '{rname}' 面积过小，计数标注在近似位置")
                    members = [i for i in range(4) if str(i + 1) in mkey]
                    pos = (sum(ells[i][0] for i in members) / len(members),
                           sum(ells[i][1] for i in members) / len(members))
                else:
                    zero_regions.append(rname)
                    continue
            if area_mode and cnt <= 0:
                zero_regions.append(rname)
                continue
            label_plan.append((mkey, cnt, pos))
    spread = _declutter_points({mk: p for mk, _c, p in label_plan})
    for mk, cnt, _p in label_plan:
        ax.annotate(str(cnt), spread[mk], fontsize=fs, ha="center", va="center",
                    fontweight="bold", color="#333333", zorder=6)
    if zero_regions and area_mode:
        _warn(f"venn --area: 区域 {zero_regions} 计数为 0，无对应面积，图中省略数字")

    for i, k in enumerate(keys):
        cx, cy, a_i, _b, _th = ells[i]
        dx, dy = cx - 0.5, cy - 0.5
        norm = _m.hypot(dx, dy)
        if norm < 1e-9:
            dx, dy, norm = 0.0, 1.0, 1.0
        dist = norm + a_i + 0.035  # 椭圆尖端外侧——计数在区域质心，两者不相撞
        lx = 0.5 + dx / norm * dist
        ly = 0.5 + dy / norm * dist
        lx = min(1.06, max(-0.06, lx))
        ly = min(1.06, max(-0.06, ly))
        ax.annotate(k, (lx, ly), fontsize=fs, fontweight="bold",
                    ha="center", va="center",
                    fontproperties=_fp(cjk_fp, k), color="#333333", zorder=5)


def gen_venn(data, ax, theme, cjk_fp, **kwargs):
    """韦恩图（2~4 集合；4 集合为椭圆布局，v2.8）。默认等圆/等椭圆示意、区域数字精确；--area 开面积比例
    （Euler）模式：圆的大小与交集面积按区域计数比例（2 集合解析解，
    3 集合圆心+半径联合最优拟合）。

    数据两种格式（二选一）:
      {"sets": {"A": [元素...], "B": [...]}} —— 元素列表，自动求交并（2~3 集合）
      {"regions": {"A": 30, "B": 25, "AB": 9}} —— 全部区域计数：
        2 集合恰 3 键 {A, B, A+B}；3 集合恰 7 键 {A,B,C,A+B,A+C,B+C,A+B+C}。
        （v2.3 的数字型 sets 因键数歧义从未可用，v2.5 起以独立键 'regions' 修复）
    """
    import matplotlib.patches as mpatches
    sets = data.get("sets", None)
    regs = data.get("regions", None)
    keys = None
    if isinstance(sets, dict) and 2 <= len(sets) <= 4 and all(
            isinstance(v, (list, tuple, set)) for v in sets.values()):
        if regs is not None:
            raise ValueError("venn: 'sets' 与 'regions' 只能二选一")
        keys = [str(k) for k in sets.keys()]
        ss = {k: set(sets[k]) for k in keys}
        regions = {}
        if len(keys) == 2:
            A, B = ss[keys[0]], ss[keys[1]]
            regions = {keys[0]: len(A - B), keys[1]: len(B - A),
                       keys[0] + keys[1]: len(A & B)}
        elif len(keys) == 3:
            A, B, C = ss[keys[0]], ss[keys[1]], ss[keys[2]]
            regions = {keys[0]: len(A - B - C), keys[1]: len(B - A - C),
                       keys[2]: len(C - A - B),
                       keys[0] + keys[1]: len((A & B) - C),
                       keys[0] + keys[2]: len((A & C) - B),
                       keys[1] + keys[2]: len((B & C) - A),
                       keys[0] + keys[1] + keys[2]: len(A & B & C)}
        else:  # v2.8：4 集合 → 15 区域
            import itertools as _it4
            for _n in (1, 2, 3, 4):
                for _combo in _it4.combinations(range(4), _n):
                    _inter = set(ss[keys[_combo[0]]])
                    for _i in _combo[1:]:
                        _inter &= ss[keys[_i]]
                    for _i in range(4):
                        if _i not in _combo:
                            _inter -= ss[keys[_i]]
                    regions["".join(keys[_i] for _i in _combo)] = len(_inter)
    elif isinstance(sets, dict):
        _nsets = len(sets) if isinstance(sets, dict) else 0
        _hint = ("；≥5 集合请改用 -t upset（v4.7 UpSet 交集图）" if _nsets > 4 else "")
        raise ValueError("venn: 'sets' 需为 2~4 个集合、值为元素列表的字典"
                         + _hint + "；区域计数请改用 'regions' 键")
    elif isinstance(regs, dict):
        all_keys = [str(k) for k in regs.keys()]
        for k in all_keys:
            v = regs[k]
            if not isinstance(v, (int, float)) or v < 0:
                raise ValueError(f"venn: 区域 '{k}' 需为非负数字（元素个数）")
        found = None
        if len(all_keys) == 3:
            for a in all_keys:
                for b in all_keys:
                    if a == b:
                        continue
                    if {a, b, a + b} == set(all_keys):
                        found = [a, b]  # 集合名只有两个，第三个键是交集计数
                        break
                if found:
                    break
        elif len(all_keys) == 7:
            for a in all_keys:
                for b in all_keys:
                    for c in all_keys:
                        if a == b or b == c or a == c:
                            continue
                        need = {a, b, c, a + b, a + c, b + c, a + b + c}
                        if need == set(all_keys):
                            found = [a, b, c]
        elif len(all_keys) == 15:  # v2.8：4 集合 15 区域
            import itertools as _it4
            for _names in _it4.permutations(all_keys, 4):
                _need = set()
                for _n in (1, 2, 3, 4):
                    for _combo in _it4.combinations(_names, _n):
                        _need.add("".join(_combo))
                if _need == set(all_keys):
                    found = list(_names)
                    break
        if not found:
            raise ValueError("venn: 'regions' 键名不构成合法区域集——2 集合需恰 "
                             "{A, B, A+B} 三键；3 集合需恰 {A,B,C,A+B,A+C,B+C,"
                             "A+B+C} 七键；4 集合需恰 15 键（A,B,C,D,A+B,…,A+B+C+D；"
                             "当前: " + ",".join(all_keys) + "）")
        keys = found
        regions = {r: int(regs[r]) for r in all_keys}
    else:
        raise ValueError("venn: 需要 'sets'（元素列表字典）或 'regions'（区域计数）")

    def _fallback_pos(region, keys, centers):
        parts = [keys.index(k) for k in keys if k in region] or [0]
        n = len(parts)
        return (sum(centers[i][0] for i in parts) / n,
                sum(centers[i][1] for i in parts) / n)

    colors = theme["colors"][:len(keys)]
    fs = theme["font_size"] + 2
    area_mode = bool(kwargs.get("area_mode"))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal"); ax.axis("off")
    if len(keys) == 4:  # v2.8 D1：4 集合走椭圆布局（默认与 --area 皆支持）
        _gen_venn4(ax, keys, regions, colors, fs, cjk_fp, area_mode)
        return

    if area_mode:
        # ── Euler 面积比例模式：圆的大小与交集面积按计数比例 ──
        import math as _m
        if len(keys) == 2:
            k1, k2 = keys
            centers, radii, vnotes = _venn2_geometry(regions[k1], regions[k2],
                                                     regions[k1 + k2])
            all_r = max(radii)
            xs = [c[0] for c in centers]
            ys = [c[1] for c in centers]
            box = (min(xs) - all_r - 0.05, min(ys) - all_r - 0.05,
                   max(xs) + all_r + 0.05, max(ys) + all_r + 0.05)
            areas, cents, _cell = _venn_region_masks(centers, radii, box, 900)
            cent_by_key = {k1: cents["1"], k2: cents["2"], k1 + k2: cents["12"]}
            fit_err = None
        else:
            k1, k2, k3 = keys
            centers, radii, fit = _venn3_geometry(regions, keys)
            idx = {k1: "1", k2: "2", k3: "3", k1 + k2: "12", k1 + k3: "13",
                   k2 + k3: "23", k1 + k2 + k3: "123"}
            cent_by_key = {rk: fit["centroids"][mk] for rk, mk in idx.items()}
            fit_err = fit["max_rel_err"]
            vnotes = []
        for msg in vnotes:
            _warn(f"venn --area: {msg}")
        if fit_err is not None:
            if fit_err <= 0.05:
                print(f"venn --area: 面积比例拟合完成（最大区域面积偏差 {fit_err*100:.1f}%）",
                      file=sys.stderr)
            else:
                _warn(f"venn --area: 区域计数在几何上难以完全按比例呈现，已取最优拟合"
                      f"（最大面积偏差 {fit_err*100:.1f}%）；区域数字仍为精确计数")
        for i, k in enumerate(keys):
            cx, cy = centers[i]
            r_draw = max(radii[i], 0.012)
            ax.add_patch(mpatches.Circle((cx, cy), r_draw, facecolor=colors[i],
                                         edgecolor="#333333", linewidth=1.4,
                                         alpha=0.42, zorder=2))
        # 集合名：沿 圆心→图心 反向推到圆外（角度逐个微错开防同心/子集情形相撞）
        for i, k in enumerate(keys):
            cx, cy = centers[i]
            r_draw = max(radii[i], 0.012)
            dx, dy = cx - 0.5, cy - 0.5
            norm = _m.hypot(dx, dy) or 1.0
            ang = _m.atan2(dy / norm, dx / norm) + i * 0.25
            lx = cx + _m.cos(ang) * (r_draw + 0.10)
            ly = cy + _m.sin(ang) * (r_draw + 0.10)
            ax.annotate(k, (lx, ly), fontsize=fs, fontweight="bold",
                        ha="center", va="center",
                        fontproperties=_fp(cjk_fp, k), color="#333333", zorder=5)
        # 区域计数：放网格质心（视觉中心即数学中心）
        zero_regions = [r for r, v in regions.items() if v <= 0]
        for region, cnt in regions.items():
            if cnt <= 0:
                continue
            pos = cent_by_key.get(region)
            if pos is None:
                pos = _fallback_pos(region, keys, centers)
                _warn(f"venn --area: 区域 '{region}' 面积过小，计数标注在近似位置")
            ax.annotate(str(cnt), pos, fontsize=fs, ha="center", va="center",
                        fontweight="bold", color="#333333", zorder=6)
        if zero_regions:
            _warn(f"venn --area: 区域 {zero_regions} 计数为 0，无对应面积，图中省略数字")
    else:
        # ── 等圆示意模式（默认）：区域数字精确，面积不按比例 ──
        if len(keys) == 2:
            centers = [(0.62, 0.5), (0.38, 0.5)]
            r = 0.27
            # 区域标签绝对坐标（与圆心几何对应）
            k1, k2 = keys
            label_xy = {k1: (0.76, 0.5), k2: (0.24, 0.5), k1 + k2: (0.5, 0.5)}
        else:
            centers = [(0.60, 0.62), (0.40, 0.62), (0.50, 0.40)]
            r = 0.235
            k1, k2, k3 = keys
            label_xy = {k1: (0.745, 0.64), k2: (0.255, 0.64), k3: (0.50, 0.245),
                        k1 + k2: (0.50, 0.705), k1 + k3: (0.585, 0.462),
                        k2 + k3: (0.415, 0.462), k1 + k2 + k3: (0.50, 0.535)}
        # 标签偏移与圈位同侧：圈1 在右(0.60)、圈2 在左(0.40)、圈3 在下——
        # 旧版偏移镜像导致前两个集合的名称互相标到对方的圈上（标签-圈错位 bug）
        label_pos = [(0.24, 0.16), (-0.24, 0.16), (0.0, -0.26)] if len(keys) == 3 \
            else [(0.24, 0.0), (-0.24, 0.0)]
        for i, k in enumerate(keys):
            cx, cy = centers[i]
            ax.add_patch(mpatches.Circle((cx, cy), r, facecolor=colors[i],
                                         edgecolor="#333333", linewidth=1.4,
                                         alpha=0.42, zorder=2))
            lx, ly = label_pos[i]
            ax.annotate(k, (cx + lx * 1.15, cy + ly * 1.15), fontsize=fs,
                        fontweight="bold", ha="center", va="center",
                        fontproperties=_fp(cjk_fp, k), color="#333333", zorder=5)
        for region, cnt in regions.items():
            lx, ly = label_xy[region]
            ax.annotate(str(cnt), (lx, ly), fontsize=fs,
                        ha="center", va="center", fontweight="bold", color="#333333",
                        zorder=6)
    total = sum(regions.values())
    # v4.6：n 消歧义——单写数字易误读为样本量，明示"并集元素总数"
    if not data.get("title"):
        _has_cjk_txt = any(any("\u4e00" <= ch <= "\u9fff" for ch in str(s)) for s in (sets or {}).keys())
        _vn = f"共 {total} 项（并集元素数）" if _has_cjk_txt else f"n = {total} (union of set elements)"
        ax.set_title(_vn)
    return None


# ── cluster_heatmap 聚类热图 ──────────────────────────────────────────

def gen_cluster_heatmap(data, ax, theme, cjk_fp, **kwargs):
    """聚类热图：行列按层次聚类（Ward）重排后绘制（v2.3 不含树状图面板，
    聚类顺序写入 stderr 与 alt 文本；树状图面板计划 v2.4）。

    数据格式同 heatmap：{"matrix": [[...]], "row_labels": [...], "col_labels": [...]}。
    """
    from scipy.cluster.hierarchy import linkage, leaves_list
    matrix = data.get("matrix", data.get("data", data.get("values", None)))
    if matrix is None or not isinstance(matrix, (list, tuple)) or len(matrix) == 0:
        raise ValueError("cluster_heatmap: 需要 'matrix'（二维数值数组）")
    M = np.asarray(matrix, dtype=float)
    if M.ndim != 2 or M.shape[0] < 2 or M.shape[1] < 2:
        raise ValueError(f"cluster_heatmap: 矩阵需 >=2×2（当前 {M.shape}）")
    if M.shape[0] > MAX_CLUSTER_ROWS:
        raise ValueError(f"cluster_heatmap: 行数 {M.shape[0]} 超过聚类上限 {MAX_CLUSTER_ROWS}"
                         f"（层次聚类内存随行数平方增长，请先筛选特征/样本；"
                         f"或加 --downsample 2000 等距采样到 2000 行后重试）")
    if np.any(~np.isfinite(M)):
        raise ValueError("cluster_heatmap: 矩阵含 NaN/Inf——请先补全（聚类不支持缺失值）")
    row_labels = list(data.get("row_labels", data.get("rows", data.get("y_labels", []))))
    col_labels = list(data.get("col_labels", data.get("cols", data.get("x_labels", []))))

    method = kwargs.get("cluster_method", "ward")
    metric = kwargs.get("cluster_metric", "euclidean")
    row_order = np.array(leaves_list(linkage(M, method=method, metric=metric)))
    col_order = np.array(leaves_list(linkage(M.T, method=method, metric=metric)))
    M2 = M[np.ix_(row_order, col_order)]
    rl2 = [row_labels[i] if i < len(row_labels) else f"行{i+1}" for i in row_order]
    cl2 = [col_labels[i] if i < len(col_labels) else f"列{i+1}" for i in col_order]

    ax._af_category_axis = True  # 行列标签是数据：豁免 fix_tick_overlaps 降级
    cmap = kwargs.get("cmap") or "RdBu_r"
    vmin = kwargs.get("vmin", None) or float(M2.min())
    vmax = kwargs.get("vmax", None) or float(M2.max())
    if vmin == vmax:
        vmin, vmax = vmin - 1e-9, vmax + 1e-9
    im = ax.imshow(M2, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
                   interpolation="nearest")
    ax.set_xticks(range(len(cl2)))
    ax.set_xticklabels(cl2, rotation=45, ha="right",
                       fontsize=max(6, theme["font_size"] - 2),
                       fontproperties=_fp(cjk_fp, " ".join(map(str, cl2))))
    ax.set_yticks(range(len(rl2)))
    # v4.6 P3：行数多时行标签字号自适应缩小（>60 行缩 1 号、>120 行缩 2 号——可读性）
    _yfs = max(5, theme["font_size"] - 2)
    if len(rl2) > 60:
        _yfs = max(5, theme["font_size"] - 3)
    if len(rl2) > 120:
        _yfs = max(4.5, theme["font_size"] - 4)
    # 无 CJK 时用 fontsize kwarg；有 CJK 时复制 cjk_fp 并设字号（None 不能 set_size）
    if cjk_fp is not None:
        _fp_row = cjk_fp.copy()
        _fp_row.set_size(_yfs)
        ax.set_yticklabels(rl2, fontproperties=_fp_row)
    else:
        ax.set_yticklabels(rl2, fontsize=_yfs)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if kwargs.get("show_values"):
        for i in range(M2.shape[0]):
            for j in range(M2.shape[1]):
                ax.text(j, i, f"{M2[i, j]:.1f}", ha="center", va="center",
                        fontsize=max(5, theme["font_size"] - 3),
                        color="white" if abs(M2[i, j] - (vmin+vmax)/2) > (vmax-vmin)/4 else "#333333")
    _warn(f"cluster_heatmap: 行聚类顺序 {rl2[:8]}{'…' if len(rl2) > 8 else ''}；"
          f"列聚类顺序 {cl2[:8]}{'…' if len(cl2) > 8 else ''}（method={method}/{metric}）")
    return im  # 交给主流程挂色条


# ── 注册表 ────────────────────────────────────────────────────────────

def gen_rmst(data, ax, theme, cjk_fp, **kwargs):
    """RMST 限制平均生存时间图（阶梯 S 曲线+τ 截断阴影 AUC+两臂差值推断；
    v5.9 第 38 号图型）。

    PH 假设不成立/曲线交叉时，单一 Cox HR 会掩盖时变效应——RMST(τ)=∫₀^τ S(u)du
    给出「到 τ 时刻平均生存多久」的绝对差，临床可解释且不依赖比例风险假设。
    数据：groups={组名: [[时间,事件(1/0)],...]}（恰好两臂，契约同 km）；
    可选 tau（截断时间；缺省=最小最大随访之半并显著告知）、time_unit。
    stderr 报告每臂 RMST(95%CI)+ΔRMST 差值（Greenwood 方差，SE=√(V₁+V₂)，
    正态近似 p）；随访不足 τ 的臂平尾外推并显著标注。多臂分组请用 -t km。"""
    has_cjk = None
    try:
        from af_shared import has_cjk as _has_cjk
        has_cjk = _has_cjk
    except ImportError:
        pass

    def _fatal(msg):
        raise ValueError(f"rmst: {msg}")

    groups = data.get("groups", data.get("series", {}))
    if not isinstance(groups, dict) or len(groups) != 2:
        _fatal("需要 groups 恰好两个组（{组名: [[时间,事件(1/0)],...]}）——"
               "RMST 是两臂对比工具，多臂请拆分或用 -t km")
    names = list(groups.keys())
    for gname in names:
        pairs = groups[gname]
        if not isinstance(pairs, (list, tuple)) or len(pairs) < 5:
            _fatal(f"组「{gname}」至少需要 5 例 [时间,事件] 对（当前 {len(pairs) if isinstance(pairs, list) else '非数组'}）")
        for p in pairs:
            if not (isinstance(p, (list, tuple)) and len(p) >= 2
                    and all(isinstance(x, (int, float)) for x in p[:2])):
                _fatal(f"组「{gname}」存在非 [时间,事件] 数值对")

    time_unit = str(data.get("time_unit", "天"))
    t_all, e_all, a_all = [], [], []
    for i, gname in enumerate(names):
        for p in groups[gname]:
            t_all.append(float(p[0]))
            e_all.append(float(p[1]))
            a_all.append(float(i))
    tau = kwargs.get("rmst_tau") or data.get("tau")
    tau_auto = False
    if tau in (None, "", "auto"):
        mx = min(max(float(p[0]) for p in groups[g]) for g in names)
        tau = mx / 2.0
        tau_auto = True
    tau = float(tau)
    if tau <= 0:
        _fatal(f"τ 须为正数（收到：{tau}）")

    res = st.rmst_analysis(t_all, e_all, a_all, tau)
    g_res = {g["name"]: g for g in res["groups"]}

    def _fmt(v):
        return f"{v:.0f}" if abs(v - round(v)) < 1e-9 else f"{v:.1f}"

    # ── 曲线（阶梯，裁剪到 τ；阴影=RMST 视觉面积）──
    for i, gname in enumerate(names):
        c = theme["colors"][i % len(theme["colors"])]
        pairs = sorted(([float(p[0]), float(p[1])] for p in groups[gname]))
        t_seq, s_seq, _cn = st.km_estimate([p[0] for p in pairs], [p[1] for p in pairs])
        keep = t_seq <= tau
        ts = list(t_seq[keep]) + ([tau] if t_seq[keep][-1] < tau else [])
        ss = list(s_seq[keep]) + ([s_seq[keep][-1]] * (1 if ts[-1] == tau and t_seq[keep][-1] < tau else 0))
        ax.step(ts, ss, where="post", color=c, linewidth=2, label=gname, zorder=3)
        ax.fill_between(ts, ss, 0, step="post", color=c, alpha=0.22,
                        hatch="///" if i > 0 else None, ec="none", zorder=2)  # v7.8.1 AF15：双臂面积可辨

    ax.axvline(tau, color="#8A8A8A", linestyle="--", linewidth=1.2, zorder=1)
    ax.set_xlim(0, tau * 1.06)                      # 右留白：τ 线不贴边
    ax.set_ylim(-0.02, 1.14)                        # 顶部预留带：τ 标签与注释框分层（视觉门 10-23）
    ax.text(tau, 1.10, f"τ={_fmt(tau)}{time_unit}", ha="center", va="bottom",
            fontsize=theme["font_size"] - 1,
            fontproperties=cjk_fp if cjk_fp and (not has_cjk or has_cjk(f"τ{_fmt(tau)}{time_unit}")) else None)

    # ── 注释框：每臂 RMST(95%CI) + ΔRMST ──
    gr = res["groups"]
    box = [f"RMST（τ={_fmt(tau)}{time_unit}）"]
    for g, nm in zip(gr, names):
        ex = "，平尾外推" if g["extrapolated"] else ""
        box.append(f"{nm}: {_fmt(g['rmst'])}（95%CI {_fmt(g['ci_low'])}~{_fmt(g['ci_high'])}）{ex}")
    if res["difference"]:
        dd = res["difference"]
        p_disp = f"P={dd['p']:.3f}" if dd["p"] >= 0.001 else "P<0.001"
        box.append(f"ΔRMST（{dd['arm_hi']}−{dd['arm_ref']}）= {_fmt(dd['diff'])} {time_unit}")
        box.append(f"（95%CI {_fmt(dd['ci_low'])}~{_fmt(dd['ci_high'])}，{p_disp}）")
    if tau_auto:
        box.append("τ 自动=最小最大随访之半（--rmst-tau 可指定）")
        print("rmst: τ 为自动值——ΔRMST 结论对 τ 敏感时请以 --rmst-tau 在多个随访阈值复核", file=sys.stderr)
    fp = cjk_fp if cjk_fp else None
    ax.text(0.98, 0.90, "\n".join(box), transform=ax.transAxes, ha="right", va="top",
            fontsize=theme["font_size"] - 1, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FBF7EF",
                      edgecolor=theme["colors"][0], linewidth=1.2, alpha=0.95),
            fontproperties=fp if fp and (not has_cjk or has_cjk("\n".join(box))) else None)

    ax.set_xlabel(f"时间（{time_unit}）", fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp else None)
    ax.set_ylabel("生存概率", fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp else None)
    ax.grid(True, alpha=0.3, linewidth=0.6)
    ax.legend(loc="lower left", fontsize=theme["font_size"] - 1, framealpha=0.9)

    # ── stderr 报告 ──
    print(f"rmst: τ={_fmt(tau)}{time_unit}" + ("（自动=最小最大随访之半）" if tau_auto else ""),
          file=sys.stderr)
    for g, nm in zip(gr, names):
        cov = f"，随访覆盖 {g['coverage'] * 100:.0f}%" + ("，⚠ 平尾外推" if g["extrapolated"] else "")
        print(f"  {nm}: RMST={_fmt(g['rmst'])}{time_unit}"
              f"（95%CI {_fmt(g['ci_low'])}~{_fmt(g['ci_high'])}，n={g['n']}，事件={g['n_events']}{cov}）",
              file=sys.stderr)
    if res["difference"]:
        dd = res["difference"]
        print(f"  ΔRMST（{dd['arm_hi']}−{dd['arm_ref']}）={_fmt(dd['diff'])}{time_unit}"
              f"（95%CI {_fmt(dd['ci_low'])}~{_fmt(dd['ci_high'])}），Z={dd['z']:.3f}，"
              + (f"P={dd['p']:.3f}" if dd["p"] >= 0.001 else "P<0.001"), file=sys.stderr)
    print("  提示：RMST 不依赖比例风险假设；τ 为临床预设的截断时间，报告中应说明选取依据。",
          file=sys.stderr)


def gen_rob(data, ax, theme, cjk_fp, **kwargs):
    """偏倚风险交通灯图（Risk of Bias traffic light；v6.1 第 39 号图型，robvis 同款）。

    系统综述/Meta 分析的纳入研究方法学质量可视化：左=研究×域交通灯网格
    （圆点着色：低风险/有顾虑/高风险/无信息），右下=加权摘要条（各域占比，
    Overall 列只入网格不入摘要——robvis 惯例）。数据：
      studies=[{name, judgements:{域键: 判定}}...]（2~50 项），
      domains=["D1",...] 或 [{key,label}...]（2~12 域；缺省=取自首个研究的键序），
      title 可选。摘要条=各域判定占比（robvis 默认等权，无自定权重语义）。
    判定取值（大小写/中英不敏感）：Low/L/低风险/低；Some concerns/S/有一定顾虑/中等；
    High/H/高风险/高；No information/NI/N/无信息/未知。配色固定语义
    （绿=低/琥珀=顾虑/红=高/灰=无信息），与主题无关。"""
    import matplotlib.patches as _mp

    def _fatal(msg):
        raise ValueError(f"rob: {msg}")

    studies = data.get("studies")
    if not isinstance(studies, list) or not (2 <= len(studies) <= 50):
        _fatal("需要 studies（2~50 个 {name, judgements} 对象）")
    dom_spec = data.get("domains")
    if dom_spec is None:
        dom_spec = [k for k in studies[0].get("judgements", {}) if k != "Overall"]
    doms = []
    for d in dom_spec:
        if isinstance(d, str):
            doms.append((d, d))
        elif isinstance(d, dict) and d.get("key"):
            doms.append((str(d["key"]), str(d.get("label", d["key"]))))
        else:
            _fatal(f"domains 每项须为字符串或 {{key,label}}（收到：{d!r}）")
    if not (2 <= len(doms) <= 12):
        _fatal(f"需要 2~12 个偏倚域（当前 {len(doms)}）")
    dkeys = [k for k, _ in doms]

    _MAP = {}
    for codes, code in ((("low", "l", "低风险", "低"), "L"),
                        (("some concerns", "someconcerns", "s", "有一定顾虑", "中等", "顾虑",
                          "unclear", "unclear risk", "不明确", "风险不明确"), "S"),
                        (("high", "h", "高风险", "高"), "H"),
                        (("very high", "veryhigh", "v", "critical", "极高风险", "极高", "危急"), "VH"),
                        (("no information", "noinformation", "ni", "n", "无信息", "未知", "不清楚"), "NI")):
        for c in codes:
            _MAP[c] = code
    # 固定语义配色：绿=低/琥珀=顾虑（含旧工具 Unclear）/红=高/深红=极高(VH)/灰=无信息
    _COLOR = {"L": "#1F7A4D", "S": "#E8A020", "H": "#B23434", "VH": "#6E1414", "NI": "#9AA0A6"}
    _LETTER = {"L": "L", "S": "S", "H": "H", "VH": "V", "NI": "?"}

    def _norm(v):
        if v is None:
            return None
        return _MAP.get(str(v).strip().lower())

    has_overall = any("Overall" in s.get("judgements", {}) for s in studies)
    rows = []
    for s in studies:
        if not isinstance(s, dict) or not s.get("name") or not isinstance(s.get("judgements"), dict):
            _fatal("studies 每项须为含 name 与 judgements 的对象")
        j = s["judgements"]
        row = {}
        for k in dkeys:
            if k not in j:
                _fatal(f"研究「{s['name']}」缺少域「{k}」的判定——所有研究须覆盖全部域")
            code = _norm(j[k])
            if code is None:
                _fatal(f"研究「{s['name']}」域「{k}」判定值「{j[k]}」无法识别——"
                       "合法：Low/L/低风险、Some concerns/S/有一定顾虑（含 Unclear）、High/H/高风险、"
                       "Very high/V/极高风险、No information/NI/无信息")
            row[k] = code
        if has_overall:
            code = _norm(j.get("Overall"))
            if code is None:
                _fatal(f"研究「{s['name']}」Overall 判定值无法识别")
            row["Overall"] = code
        rows.append((str(s["name"]), row))

    # ── 摘要计数（Overall 不入摘要——robvis 惯例；等权占比）──
    counts = {k: {"L": 0, "S": 0, "H": 0, "VH": 0, "NI": 0} for k in dkeys}
    for _, row in rows:
        for k in dkeys:
            counts[k][row[k]] += 1

    # ── 布局：上=交通灯网格，下=加权摘要条（共享域 x 轴）──
    n = len(rows)
    x_overall = len(dkeys) - 1 + 0.7 if has_overall else None
    ax.set_xlim(-0.55, (x_overall if has_overall else len(dkeys) - 1) + 0.55)
    ax.set_ylim(-1.9, n - 0.4)
    # 手排：研究 i（0 起）→ y=i（顶部=0，ylim 反向）；摘要区在网格下方
    y_sum0, y_sum1 = n + 0.35, n + 1.45          # 摘要条带
    ax.set_ylim(n + 1.9, -0.7)                    # 顶大底小：研究 1 在最上
    for i, (name, row) in enumerate(rows):
        for ci, k in enumerate(dkeys):
            code = row[k]
            ax.scatter(ci, i, s=300, c=_COLOR[code], edgecolors="white",
                       linewidths=1.6, zorder=3)
            ax.text(ci, i, _LETTER[code], ha="center", va="center",
                    fontsize=theme["font_size"] - 3, color="white",
                    fontweight="bold", zorder=4)
        if has_overall:
            code = row["Overall"]
            xo = x_overall
            ax.scatter(xo, i, s=300, c=_COLOR[code], edgecolors="white",
                       linewidths=1.6, zorder=3)
            ax.text(xo, i, _LETTER[code], ha="center", va="center",
                    fontsize=theme["font_size"] - 3, color="white",
                    fontweight="bold", zorder=4)
    if has_overall:
        ax.plot([x_overall - 0.35, x_overall - 0.35], [-0.55, n - 0.55],
                color="#C9C2B4", linewidth=1.0, zorder=1)

    # 摘要条（加权占比；Low 贴基线向上堆叠）
    order = ["L", "S", "H", "VH", "NI"]            # 自基线向上：低、顾虑、高、极高、无信息
    base = y_sum1
    htot = y_sum1 - y_sum0
    # v7.8.2 AF18（复测修正）：标签放条带上方单行（ylim 反向：视觉上方=y_sum0 侧）——v7.8.1 的段内两行标签
    # 在薄条带里被相邻段裁切/重叠（复测实锤）。每域标最大段（≥15%），次段靠
    # 颜色+图例，计数明细在 stderr。
    _dom_label = {}
    for ci, k in enumerate(dkeys):
        _max_code = max(order, key=lambda c: counts[k][c])
        if counts[k][_max_code] / n >= 0.15:
            _dom_label[ci] = counts[k][_max_code] / n
    for ci, k in enumerate(dkeys):
        cum = 0.0
        for code in order:
            h = counts[k][code] / n * htot         # 占比×条带高
            if h <= 0:
                continue
            ax.bar(ci, h, bottom=base - cum - h, width=0.62,
                   color=_COLOR[code], edgecolor="white", linewidth=0.8, zorder=3)
            cum += h
    for ci, _frac in _dom_label.items():
        ax.text(ci, y_sum0 - 0.14, f"{_frac * 100:.0f}%（{counts[dkeys[ci]][max(order, key=lambda c: counts[dkeys[ci]][c])]}/{n}）",
                ha="center", va="bottom", fontsize=max(5.0, theme["font_size"] - 2),
                color="#333333", zorder=4,
                fontproperties=cjk_fp if cjk_fp else None)
    if has_overall:
        oc = {"L": 0, "S": 0, "H": 0, "VH": 0, "NI": 0}
        for _, row in rows:
            oc[row["Overall"]] += 1
        _max_code = max(order, key=lambda c: oc[c])
        cum = 0.0
        for code in order:
            h = oc[code] / n * htot
            if h <= 0:
                continue
            ax.bar(x_overall, h, bottom=base - cum - h, width=0.62,
                   color=_COLOR[code], edgecolor="white", linewidth=0.8, zorder=3)
        if oc[_max_code] / n >= 0.15:
            ax.text(x_overall, y_sum0 - 0.14,
                    f"{oc[_max_code] / n * 100:.0f}%（{oc[_max_code]}/{n}）",
                    ha="center", va="bottom", fontsize=max(5.0, theme["font_size"] - 2),
                    color="#333333", zorder=4,
                    fontproperties=cjk_fp if cjk_fp else None)

    ax.axhline(y_sum1, color="#8A8A8A", linewidth=1.0, xmin=0.0,
               xmax=1.0, zorder=2)
    # 坐标轴
    ax.set_yticks(list(range(n)))
    ax.set_yticklabels([nm for nm, _ in rows], fontsize=theme["font_size"] - 1,
                       fontproperties=cjk_fp if cjk_fp else None)
    xticks = list(range(len(dkeys))) + ([x_overall] if has_overall else [])
    xlabels = [lab for _, lab in doms] + (["Overall 总体"] if has_overall else [])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, fontsize=theme["font_size"] - 2, rotation=18,
                       ha="right", fontproperties=cjk_fp if cjk_fp else None)
    ax.set_xticks([x + 0.5 for x in range(len(dkeys) - 1)], minor=True)
    ax.grid(True, axis="x", which="minor", alpha=0.25, linewidth=0.5)
    ax.tick_params(axis="y", length=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)

    _LB = {"L": "低风险 Low", "S": "顾虑/Unclear", "H": "高风险 High",
           "VH": "极高风险 Very high", "NI": "无信息 No information"}
    # ⛔勿用外层循环变量 k（泄漏=只查最后一个域，图例漏档事故 10-26）：显式全域扫描
    present = [c for c in ("L", "S", "H", "VH", "NI")
               if any(row[dk] == c for _, row in rows for dk in dkeys)
               or (has_overall and any(row["Overall"] == c for _, row in rows))]
    handles = [_mp.Patch(facecolor=_COLOR[c], edgecolor="white",
                         label=_LB[c]) for c in present]
    # 图例放图下方外侧（robvis 惯例；bbox_inches='tight' 会完整收入，且不遮摘要条）
    leg = ax.legend(handles=handles, loc="upper center",
                    bbox_to_anchor=(0.5, -0.28), fontsize=theme["font_size"] - 2,
                    framealpha=0.95, ncol=4)
    if cjk_fp:
        try:
            leg.set_prop(cjk_fp)
        except Exception:
            pass
    ttl = str(data.get("title") or "偏倚风险图 Risk of Bias（交通灯）")
    ax.set_title(ttl, fontsize=theme["font_size"] + 1,
                 fontproperties=cjk_fp if cjk_fp and _has_cjk(ttl) else None)

    # ── stderr 报告 ──
    print(f"rob: {n} 项研究 × {len(dkeys)} 个偏倚域"
          + ("（含 Overall 列，未计入摘要）" if has_overall else ""), file=sys.stderr)
    for ci, k in enumerate(dkeys):
        c = counts[k]
        pr = {code: c[code] / n * 100 for code in ("L", "S", "H", "VH", "NI")}
        lab = dict(doms)[k]
        print(f"  {lab}: 低 {pr['L']:.0f}%（{c['L']}）｜顾虑 {pr['S']:.0f}%（{c['S']}）"
              f"｜高 {pr['H']:.0f}%（{c['H']}）｜极高 {pr['VH']:.0f}%（{c['VH']}）"
              f"｜无信息 {pr['NI']:.0f}%（{c['NI']}）",
              file=sys.stderr)
    print("  提示：判定应来自预设的 ROB2/ROBINS-I/QUADAS-2 工具与两人独立评估；",
          file=sys.stderr)




# ── labbe L'Abbé 图（v6.3 第 40 号图型，Meta 四件套收官：forest/funnel/galbraith/labbe） ──

def gen_labbe(data, ax, theme, cjk_fp, **kwargs):
    from af_shared import fmt_ratio_ci  # v7.8.1 AF11（函数内懒加载：af_shared 顶部反向 import 本模块，顶层引会成环）
    """L'Abbé 图（处理组 vs 对照组事件率散点，Meta 分析效应直观化）。

    x=对照组事件率，y=处理组事件率；对角线 y=x 为无效应线（RR=1），
    DL 随机效应合并 RR 参考线 y=RR·x；点面积 ∝ 研究权重（1/方差）——
    一眼看出：点在对角线上=处理无效，上方=有害，下方=有益，离合并线远者=异质性嫌疑。
    数据: {"studies": [{"name": "...", "events_t": n, "n_t": n,
                        "events_c": n, "n_c": n}, ...]}
    （处理/对照组事件数与样本总数，2×2 四格表）
    选项: est_measure（RR/OR，默认 RR——logOR 尺度下参考线非线性，RR 版最直观）、
    show_labels（bool，默认 <=12 全标注）。
    """
    studies = data.get("studies", None)
    if not studies or not isinstance(studies, list):
        raise ValueError("labbe: 需要 'studies' 数组，每项含 name/events_t/n_t/events_c/n_c（2×2 四格表）")
    names, et, nt, ec, nc = [], [], [], [], []
    for i, s in enumerate(studies):
        for k, arr in (("events_t", et), ("n_t", nt), ("events_c", ec), ("n_c", nc)):
            v = s.get(k)
            if v is None or not isinstance(v, (int, float)) or v < 0:
                raise ValueError(f"labbe: 研究 {i+1}（{s.get('name', '?')}）的 {k} 非法（须为非负数）")
            arr.append(float(v))
        names.append(str(s.get("name", f"研究{i+1}")))
    et, nt, ec, nc = map(np.asarray, (et, nt, ec, nc))
    bad = (nt <= 0) | (nc <= 0) | (et > nt) | (ec > nc)
    if bad.any():
        i = int(np.where(bad)[0][0])
        raise ValueError(f"labbe: 研究 {i+1}（{names[i]}）四格表非法（事件数不得超过总数，n 须为正）")
    if len(et) < 3:
        raise ValueError("labbe: 至少需要 3 个研究（两点定不了线，三点才有异质性信息）")
    zero = (ec == 0) | (et == 0)
    if zero.all():
        raise ValueError("labbe: 全部研究的事件率均为 0 或对照全零——无法定义效应方向")
    if zero.any():
        _warn(f"labbe: {int(zero.sum())} 个研究含零事件格（事件率 0），无法取 log 参与合并，已从合并统计剔除（点仍绘出）")

    measure = str(data.get("est_measure") or "RR").upper()
    if measure not in ("RR", "OR"):
        raise ValueError("labbe: est_measure 仅支持 RR/OR")

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 2)
    c_main = theme["colors"][0]
    pt = et / nt          # 处理组事件率
    pc = ec / nc          # 对照组事件率

    # DL 随机效应合并（log 尺度；零格研究剔除）
    keep = ~zero
    rr_line = None
    pooled = None
    if keep.any():
        if measure == "RR":
            es = np.log(pt[keep] / pc[keep])
        else:
            a, b_ = et[keep], nt[keep] - et[keep]
            c_, d_ = ec[keep], nc[keep] - ec[keep]
            es = np.log((a + 0.5) / (b_ + 0.5) / ((c_ + 0.5) / (d_ + 0.5)))
        v = 1.0 / et[keep] - 1.0 / nt[keep] + 1.0 / ec[keep] - 1.0 / nc[keep]
        v = np.maximum(v, 1e-8)
        ses = np.sqrt(v)
        pooled = st.dl_pool(es, ses)
        rr = float(np.exp(pooled["pooled"]))
        lo = float(np.exp(pooled["pooled"] - 1.96 * pooled["se"]))
        hi = float(np.exp(pooled["pooled"] + 1.96 * pooled["se"]))
        hi_cap = min(hi, 1.05 * float(max(pc.max(), pt.max())))

    hi_ax = 1.08 * float(max(pc.max(), pt.max()))
    ax.plot([0, hi_ax], [0, hi_ax], color="#888888", lw=1.2, ls="--", zorder=2)
    _rl = "无效应线（RR=1）" if measure == "RR" else "无效应线（OR=1）"
    import matplotlib.patheffects as _pe
    _stroke = [_pe.withStroke(linewidth=2.2, foreground="white")]
    ax.annotate(_rl, (0.055 * hi_ax, 0.055 * hi_ax), ha="left", va="top",
                xytext=(0, -8), textcoords="offset points", fontsize=fs_s,
                color="#999999", path_effects=_stroke, zorder=2)
    if pooled is not None:
        xg = np.linspace(1e-4, hi_ax, 64)
        _e, _l, _h, _sig = fmt_ratio_ci(rr, lo, min(hi, 99), measure)
        _sig_s = "，不含 1" if _sig else ""
        ax.plot(xg, rr * xg, color=c_main, lw=1.6, zorder=3,
                label=f"合并 {measure}={_e}（{_l}~{_h}，随机效应{_sig_s}）")

    # 点面积 ∝ 研究权重（1/方差归一到 [30, 320]）
    var = np.maximum(1.0 / np.maximum(et, 1) - 1.0 / nt + 1.0 / np.maximum(ec, 1) - 1.0 / nc, 1e-8)
    w = 1.0 / var
    sizes = 30 + 290 * (w / w.max())
    ax.scatter(pc, pt, s=sizes, color=c_main, alpha=0.75,
               edgecolor="#333333", linewidth=0.9, zorder=4)
    # v7.8.1 AF13：气泡面积语义图内自解释（面积∝研究权重 1/方差）
    ax.text(0.98, 0.02, "气泡面积∝研究权重（1/方差）", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=fs_s, color="#999999")

    show_all = data.get("show_labels")
    show_all = (len(names) <= 12) if show_all is None else bool(show_all)
    # 标注朝向=远离合并线的方向（上方点标上侧、下方点标下侧）——
    # v6.3.0 视觉验收三轮教训：反着放（朝线）必压线割线（UK-1 三轮残留即此因）
    _rr_eff = rr if pooled is not None else 1.0
    _above = pt > _rr_eff * pc
    _diff = np.abs(pt - _rr_eff * pc)              # 点到合并线走廊的距离
    _on_line = _diff < 0.012   # 骑线点（RR 贴合并线走廊）
    _anns = []
    for i, nm in enumerate(names):
        if show_all:
            _fp = cjk_fp if cjk_fp and _has_cjk(nm) else None
            if _on_line[i]:
                continue  # 骑线点由下方专用引线循环处理
            if abs(pt[i] - pc[i]) < 0.02:
                # 两线夹缝点（贴无效应对角线）：上下都是参考线——引线横向左拉到空白
                _a = ax.annotate(nm, (pc[i], pt[i]), textcoords="offset points",
                                 xytext=(-26, 14), ha="right", va="bottom",
                                 fontsize=fs_s, color="#555555", fontproperties=_fp,
                                 path_effects=_stroke, zorder=6,
                                 arrowprops=dict(arrowstyle="-", lw=0.8,
                                                 color="#AAAAAA", shrinkA=1, shrinkB=3))
                _anns.append((_a, False, nm, float(pc[i]), float(pt[i]),
                              (-26, 14), "right", fs_s, "#555555", _fp, True))
                continue
            if _above[i]:
                _off, _va = ((8, 14), "bottom") if _diff[i] < 0.025 else ((8, 6), "bottom")
            else:
                _off, _va = ((8, -16), "top") if _diff[i] < 0.025 else ((8, -11), "top")
            _a = ax.annotate(nm, (pc[i], pt[i]), textcoords="offset points",
                             xytext=_off, ha="left", va=_va, fontsize=fs_s,
                             color="#555555", fontproperties=_fp,
                             path_effects=_stroke, zorder=6)
            _anns.append((_a, False, nm, float(pc[i]), float(pt[i]),
                          _off, "left", fs_s, "#555555", _fp, False))
    for i, nm in enumerate(names):
        if show_all and _on_line[i]:
            _fp = cjk_fp if cjk_fp and _has_cjk(nm) else None
            _sx, _sy = ((44, 10) if i % 2 == 0 else (44, -18))  # 奇偶交替，双骑线簇错位
            _a = ax.annotate(nm, (pc[i], pt[i]), textcoords="offset points",
                             xytext=(_sx, _sy), ha="left",
                             va="bottom" if _sy > 0 else "top",
                             fontsize=fs_s, color="#555555", fontproperties=_fp,
                             path_effects=_stroke, zorder=6,
                             arrowprops=dict(arrowstyle="-", lw=0.8,
                                             color="#AAAAAA", shrinkA=1, shrinkB=3))
            _anns.append((_a, False, nm, float(pc[i]), float(pt[i]),
                          (_sx, _sy), "left", fs_s, "#555555", _fp, True))
    # 紧凑避让（L'Abbé 专用）：小步长候选贴点重试，禁 declutter 大阶梯
    # （600dpi 下 132pt 阶梯=大幅数据位移→标注悬空，v6.3.0 首轮视觉验收抓出）
    _dropped = 0
    if len(_anns) >= 2:
        import matplotlib.patheffects as _pe2
        _st2 = [_pe2.withStroke(linewidth=2.2, foreground="white")]
        _fig = ax.figure
        _fig.canvas.draw()
        _rend = _fig.canvas.get_renderer()
        _placed = []
        for _a, _out, _nm, _xi, _zi, (_dx, _dy), _ha, _fs, _col, _fp, *_lead in _anns:
            _leader = _lead[0] if _lead else False
            _bb = _a.get_window_extent(_rend).expanded(1.10, 1.30)
            if not any(_bb.overlaps(_p) for _p in _placed):
                _placed.append(_bb)
                continue
            _a.remove()
            _va0 = "top" if _dy < 0 else "bottom"
            if _leader:
                _cands = ()  # 引线项重试仍走引线（贴位=回撞线/邻簇，v6 教训）
            else:
                _cands = (( _dx + 4, _dy), (_dx - 14, _dy), (_dx, _dy + (10 if _dy < 0 else -10)),
                          (_dx, _dy + (16 if _dy < 0 else -16)), (-_dx - 4, _dy))
            _a2 = None
            for _ox, _oy in _cands:
                _t = ax.annotate(_nm, (_xi, _zi), textcoords="offset points",
                                 xytext=(_ox, _oy), ha="left", va=_va0,
                                 fontsize=_fs, color=_col, fontproperties=_fp,
                                 path_effects=_st2, zorder=6)
                _bt = _t.get_window_extent(_rend).expanded(1.10, 1.30)
                if not any(_bt.overlaps(_p) for _p in _placed):
                    _a2 = _t
                    _placed.append(_bt)
                    break
                _t.remove()
            if _a2 is None:
                # 引线兜底（v6.3.0 视觉验收多轮教训：簇集点贴位候选会耗尽，
                # 直接省略=研究缺标注；远置+细引线=不悬空且脱离合并线/邻簇）
                for _ox, _oy in ((18, 40), (44, 8), (-20, 36), (16, -42),
                                 (-44, 10), (-44, -16), (44, -32), (8, 52)):
                    _t = ax.annotate(_nm, (_xi, _zi), textcoords="offset points",
                                     xytext=(_ox, _oy), ha="left",
                                     va="bottom" if _oy > 0 else "top",
                                     fontsize=_fs, color=_col, fontproperties=_fp,
                                     path_effects=_st2, zorder=6,
                                     arrowprops=dict(arrowstyle="-", lw=0.8,
                                                     color="#AAAAAA",
                                                     shrinkA=1, shrinkB=3))
                    _bt = _t.get_window_extent(_rend).expanded(1.10, 1.30)
                    if not any(_bt.overlaps(_p) for _p in _placed):
                        _a2 = _t
                        _placed.append(_bt)
                        break
                    _t.remove()
            if _a2 is None:
                _dropped += 1
    if _dropped:
        _warn(f"labbe: {_dropped} 个研究名与相邻标注叠印已省略（数据点仍在图上）")

    ax.set_xlim(0, hi_ax)
    ax.set_ylim(0, hi_ax)
    ax.set_aspect("equal", adjustable="box")  # 等比例（对角线视觉 45°；xlim/ylim 已显式同域）
    xl = str(data.get("x_label") or "对照组事件率")
    yl = str(data.get("y_label") or "处理组事件率")
    ax.set_xlabel(xl, fontproperties=cjk_fp if cjk_fp and _has_cjk(xl) else None)
    ax.set_ylabel(yl, fontproperties=cjk_fp if cjk_fp and _has_cjk(yl) else None)
    if ax.get_legend_handles_labels()[1]:
        ax.legend(fontsize=fs - 1, loc="upper left", framealpha=0.9, prop=cjk_fp)
    if pooled is not None:
        _warn(f"labbe: DL 随机效应合并 {measure}={rr:.4g}（95%CI {lo:.3g}~{hi:.3g}），"
              f"异质性 I²={pooled['i2']:.0f}%，P_het={pooled['p_het']:.3g}"
              f"（合并含 {int(keep.sum())}/{len(et)} 个研究）")
    return None

EXTRA_GENERATORS = {
    "funnel": gen_funnel,
    "galbraith": gen_galbraith,
    "labbe": gen_labbe,
    "cif": gen_cif,
    "rmst": gen_rmst,
    "rob": gen_rob,
    "bland_altman": gen_bland_altman,
    "pca": gen_pca,
    "paired": gen_paired,
    "venn": gen_venn,
    "cluster_heatmap": gen_cluster_heatmap,
}

EXTRA_DEMO_DATA = {
    "funnel": {"studies": [
        {"name": "Smith 2020", "effect": 0.69, "se": 0.12},
        {"name": "Lee 2021", "effect": 0.55, "se": 0.20},
        {"name": "王 2022", "effect": 0.80, "se": 0.09},
        {"name": "Garcia 2023", "effect": 0.42, "se": 0.31},
        {"name": "陈 2024", "effect": 0.61, "se": 0.15},
        {"name": "Kim 2025", "effect": 0.73, "se": 0.11},
    ]},
    "galbraith": {"est_label": "OR", "studies": [
        {"name": "Smith 2019", "effect": 0.58, "se": 0.34},
        {"name": "Lee 2020", "effect": 0.71, "se": 0.28},
        {"name": "王 2021", "effect": 0.62, "se": 0.19},
        {"name": "Garcia 2021", "effect": 0.55, "se": 0.15},
        {"name": "陈 2022", "effect": 0.67, "se": 0.12},
        {"name": "Kim 2022", "effect": 0.49, "se": 0.11},
        {"name": "Rossi 2023", "effect": 0.73, "se": 0.10},
        {"name": "Nakamura 2023", "effect": 0.60, "se": 0.09},
        {"name": "李 2024", "effect": 0.64, "se": 0.08},
        {"name": "Dubois 2024", "effect": 1.55, "se": 0.22},
    ]},
    "cif": {"time": [3, 5, 6, 7, 8, 10, 12, 12, 14, 16, 18, 20, 22, 24, 26, 28,
                      30, 32, 34, 36, 38, 40, 42, 44],
             "event": [1, 2, 1, 0, 1, 2, 0, 1, 0, 2, 1, 0, 0, 2, 1, 0,
                       2, 0, 1, 0, 0, 2, 0, 0],
             "cause_labels": {"1": "复发", "2": "移植相关死亡"},
             "time_unit": "月"},
    "bland_altman": {"methods": {"新仪器": [5.1, 4.9, 5.3, 5.6, 4.8, 5.2, 5.0, 5.5],
                                 "金标准": [5.0, 5.1, 5.2, 5.4, 5.0, 5.1, 5.2, 5.3]}},
    "pca": {"matrix": [[5.1, 3.5, 1.4, 0.2], [4.9, 3.0, 1.4, 0.2], [6.7, 3.1, 4.4, 1.4],
                        [6.0, 2.9, 4.5, 1.5], [6.3, 3.3, 6.0, 2.5], [5.8, 2.7, 5.1, 1.9],
                        [4.7, 3.2, 1.3, 0.2], [6.1, 2.8, 4.7, 1.2]],
            "groups": ["setosa", "setosa", "versicolor", "versicolor",
                       "virginica", "virginica", "setosa", "versicolor"],
            "feature_names": ["萼长", "萼宽", "瓣长", "瓣宽"]},
    "paired": {"series": {"术前": [8.2, 7.5, 9.1, 6.8, 7.9, 8.5],
                           "术后": [6.1, 5.8, 7.2, 5.0, 6.3, 6.9]}},
    "venn": {"sets": {"基因集A": ["TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN"],
                      "基因集B": ["TP53", "EGFR", "ALK", "ROS1"],
                      "基因集C": ["TP53", "MYC", "ALK", "NRAS"]}},
    "cluster_heatmap": {"matrix": [[2.1, 0.3, 1.8, 0.1], [1.9, 0.2, 2.0, 0.3],
                                    [0.2, 2.2, 0.1, 1.9], [0.3, 2.0, 0.4, 2.1],
                                    [1.8, 0.4, 1.9, 0.2], [0.1, 1.8, 0.3, 2.0]],
                         "row_labels": ["样本1", "样本2", "样本3", "样本4", "样本5", "样本6"],
                         "col_labels": ["基因A", "基因B", "基因C", "基因D"]},
}


# ── validate / alt / caption 钩子 ─────────────────────────────────────

def validate_extra(chart_type, data):
    """新图型数据校验。返回 (fatal, warn) 两条列表（信息可含修正指引）。"""
    fatal, warns = [], []
    if chart_type == "funnel":
        studies = data.get("studies", None)
        if not studies and (data.get("effects") is None or data.get("ses") is None):
            fatal.append("funnel: 需要 'studies'（每项含 name/effect/se）或 'effects'+'ses'")
        elif studies:
            bad = [i for i, s in enumerate(studies)
                   if not isinstance(s, dict) or "effect" not in s or "se" not in s]
            if bad:
                fatal.append(f"funnel: studies 第 {bad[:3]} 项缺少 effect 或 se 字段")
    elif chart_type == "galbraith":
        if not data.get("studies") and (data.get("effects") is None or data.get("ses") is None):
            fatal.append("galbraith: 需要 'studies'（每项含 name/effect/se）或 'effects'+'ses'")
        elif isinstance(data.get("studies"), list):
            if len(data["studies"]) < 3:
                fatal.append("galbraith: 至少需要 3 个研究（精度-标准化效应平面才有可读性）")
            bad = [i for i, s in enumerate(data["studies"])
                   if not isinstance(s, dict) or "effect" not in s or "se" not in s]
            if bad:
                fatal.append(f"galbraith: studies 第 {bad[:3]} 项缺少 effect 或 se 字段")
        elif isinstance(data.get("effects"), list) and len(data["effects"]) < 3:
            fatal.append("galbraith: 至少需要 3 个研究（精度-标准化效应平面才有可读性）")
        _arcs = data.get("arcs")
        if _arcs not in (None, "auto") and not isinstance(_arcs, bool):
            fatal.append("galbraith: arcs 须为 true/false/auto（默认 auto=比率尺度开弧线）")
    elif chart_type == "cif":
        t_raw = data.get("time")
        e_raw = data.get("event")
        if isinstance(data.get("groups"), dict):
            fatal.append("cif: 不支持 groups 多臂分组——CIF 按事件原因分层；"
                         "多臂竞争风险请用 -t km（内置 AJ 自动模式）")
        elif not isinstance(t_raw, list) or not isinstance(e_raw, list):
            fatal.append("cif: 需要 'time'+'event' 两个等长数组"
                         "（0=删失 1=目标事件 ≥2=竞争事件）")
        else:
            if len(t_raw) != len(e_raw):
                fatal.append(f"cif: time 有 {len(t_raw)} 个值但 event 有 "
                             f"{len(e_raw)} 个 — 长度必须一致")
            elif not t_raw:
                fatal.append("cif: 数据为空")
            else:
                _bad_t = [i for i, v in enumerate(t_raw)
                          if not isinstance(v, (int, float)) or isinstance(v, bool)
                          or v != v or v < 0]
                if _bad_t:
                    fatal.append(f"cif: time 第 {_bad_t[:3]} 项非数值/负数")
                _bad_e = [i for i, v in enumerate(e_raw)
                          if not isinstance(v, (int, float)) or isinstance(v, bool)
                          or float(v) != int(v) or v < 0]
                if _bad_e:
                    fatal.append(f"cif: event 第 {_bad_e[:3]} 项须为 ≥0 整数编码"
                                 "（0=删失 1=目标事件 ≥2=竞争事件）")
                elif not any((not isinstance(v, bool)) and isinstance(v, (int, float))
                             and v >= 1 for v in e_raw):
                    fatal.append("cif: 全部为删失（event 全 0）——无法估计累计发生率")
        _ck = data.get("compare_km")
        if _ck not in (None, "auto") and not isinstance(_ck, bool):
            fatal.append("cif: compare_km 须为 true/false/auto"
                         "（默认 auto=有竞争事件才画参照线）")
    elif chart_type == "bland_altman":
        if ("a" not in data or "b" not in data) and not isinstance(data.get("methods"), dict):
            fatal.append("bland_altman: 需要 'a'+'b' 数组或 'methods' 两个系列")
    elif chart_type == "pca":
        m = data.get("matrix")
        if not m:
            fatal.append("pca: 需要 'matrix'（行=样本 列=特征）")
        elif len(m[0]) > MAX_PCA_COLS:
            fatal.append(f"pca: 特征列 {len(m[0])} 超上限 {MAX_PCA_COLS}")
    elif chart_type == "paired":
        if ("before" not in data or "after" not in data) and not isinstance(data.get("series"), dict):
            fatal.append("paired: 需要 'before'+'after' 或 'series' 恰好两项")
    elif chart_type == "venn":
        s = data.get("sets")
        rg = data.get("regions")
        ok_sets = (isinstance(s, dict) and 2 <= len(s) <= 4 and not rg  # v2.8：4 集合
                   and all(isinstance(v, (list, tuple, set)) for v in s.values()))
        ok_regs = isinstance(rg, dict) and len(rg) in (3, 7, 15) and not s  # v2.8：15 键
        if not (ok_sets or ok_regs):
            _nsets = len(s) if isinstance(s, dict) else 0
            _hint = ("；≥5 集合请改用 -t upset（v4.7 UpSet 交集图）" if _nsets > 4 else "")
            fatal.append("venn: 需要 'sets'（2~4 个集合，值为元素列表）或 'regions'"
                         "（区域计数：2 集合恰 {A,B,A+B} 三键 / 3 集合恰 7 键 /"
                         " 4 集合恰 15 键）" + _hint)
    elif chart_type == "cluster_heatmap":
        m = data.get("matrix", data.get("data", data.get("values")))
        if m is None:
            fatal.append("cluster_heatmap: 需要 'matrix'")
        elif isinstance(m, (list, tuple)) and len(m) > MAX_CLUSTER_ROWS:
            fatal.append(f"cluster_heatmap: 行数 {len(m)} 超过聚类上限 {MAX_CLUSTER_ROWS}"
                         "（可加 --downsample 2000 等距采样后重试）")
    return fatal, warns


def alt_extra(chart_type, data, title=""):
    """新图型的无障碍描述（--alt）。"""
    t = f"{title}。" if title else ""
    if chart_type == "funnel":
        n = len(data.get("studies", data.get("effects", [])) or [])
        return f"{t}漏斗图，含 {n} 个研究的效应值散点、DerSimonian-Laird 合并效应线与 95% 伪置信漏斗线。"
    if chart_type == "galbraith":
        n = len(data.get("studies", data.get("effects", [])) or [])
        return (f"{t}Galbraith 径向图，{n} 个研究按精度（1/SE）与标准化效应排布，"
                "过原点直线为固定效应合并，±1.96 平行带覆盖同质研究，带外即离群/异质性嫌疑。")
    if chart_type == "cif":
        ev = data.get("event") or []
        _nc = sum(1 for v in ev if isinstance(v, (int, float))
                  and not isinstance(v, bool) and v == 1)
        _nx = sum(1 for v in ev if isinstance(v, (int, float))
                  and not isinstance(v, bool) and v >= 2)
        return (f"{t}竞争风险累计发生率图（Aalen-Johansen）：{len(ev)} 名受试者"
                f"（目标事件 {_nc}、竞争事件 {_nx}），各事件原因一条累计发生率阶梯曲线，"
                "虚线为 1−KM 朴素对照（竞争事件当删失，系统性高估）。")
    if chart_type == "bland_altman":
        a = data.get("a") or (data.get("methods") or {}).get(list(data.get("methods", {}))[0], [])
        return f"{t}Bland-Altman 一致性图，{len(a)} 对测量的差值-均值散点，含均值差线与 95% 一致性界线。"
    if chart_type == "pca":
        m = data.get("matrix") or []
        return f"{t}PCA 得分图，{len(m)} 个样本投影到前两个主成分平面，橙色箭头为主要载荷特征。"
    if chart_type == "paired":
        b = data.get("before") or []
        return f"{t}配对前后图，{len(b)} 个受试对象各一条灰色折线连接前后两次测量，附配对检验显著性。"
    if chart_type == "venn":
        s = data.get("sets") or {}
        return f"{t}韦恩图，{len(s)} 个集合的交并关系，各区域标注元素个数（不按面积比例）。"
    if chart_type == "cluster_heatmap":
        m = data.get("matrix") or []
        return f"{t}聚类热图，{len(m)} 行按层次聚类重排，颜色深浅映射数值高低。"
    return t or f"{chart_type} 图。"


# ── 图注模板（--caption，中英双语并列） ────────────────────────────────

def make_caption(chart_type, data, title=""):
    """期刊式图注（中英双语并列），写 <out>.caption.txt。渲染失败不阻断出图。"""
    zh_head = f"{title}。" if title else ""
    en_head = ""
    def _n(key, default="?"):
        v = data.get(key)
        return str(len(v)) if isinstance(v, (list, dict, tuple)) else default
    T = {
        "bar": ("柱状图展示各组测量值（n 组）。",
                "Bar chart of measurements across groups."),
        "box": (f"箱线图展示 {_n('series')} 组分布：箱体=四分位距，横线=中位数，须线=1.5×IQR。",
                f"Box plots of {len(data.get('series', {}) or [])} groups: box = IQR, line = median, whiskers = 1.5×IQR."),
        "violin": (f"小提琴图展示 {_n('series')} 组分布（核密度估计），内部箱线为中位数与四分位。",
                "Violin plots (kernel density) with inner box (median and IQR)."),
        "km": ("Kaplan-Meier 生存曲线（纵轴生存概率，横轴时间），下方风险表为各时间点仍处于风险的人数；log-rank 检验。",
               "Kaplan-Meier survival curves with numbers at risk; log-rank test."),
        "roc": ("ROC 曲线，AUC 量化判别能力（0.5=无判别，1.0=完美）。",
                "ROC curves; AUC quantifies discrimination."),
        "forest": ("森林图：各方块为各研究效应值（面积∝权重），横线为 95%CI，菱形为合并效应。",
                   "Forest plot: squares = study effects (area ∝ weight), lines = 95% CI, diamond = pooled effect."),
        "heatmap": ("热图，颜色深浅映射数值大小（见色条）。",
                    "Heatmap; color intensity maps value (see colorbar)."),
        "scatter": ("散点图及线性趋势线。",
                    "Scatter plot with linear trend."),
        "line": ("折线图展示随 x 变化的趋势。",
                 "Line plot of trends."),
        "funnel": ("漏斗图：各研究效应值 vs 标准误，虚线为 95% 伪置信界，竖线为 DL 随机效应合并值。",
                   "Funnel plot: study effects vs SE, dashed pseudo-95% CI bounds, vertical line = DL pooled estimate."),
        "galbraith": ("Galbraith 径向图：横轴精度 1/SE、纵轴标准化效应，过原点直线为固定效应合并，±1.96 平行带外的研究提示离群/异质性。",
                      "Galbraith radial plot: precision (1/SE) vs standardized effect; regression through origin = pooled fixed effect; studies outside the ±1.96 band suggest heterogeneity or outliers."),
        "cif": ("累计发生率图（Aalen-Johansen）：各事件原因一条阶梯曲线；虚线为 1−KM 朴素估计（竞争事件当删失，系统性高估目标事件风险）。",
                "Cumulative incidence curves by cause (Aalen-Johansen); dashed = naive 1−KM reference (competing events censored; systematically overestimates the target event)."),
        "bland_altman": ("Bland-Altman 图：横轴两法均值、纵轴差值；实线=均值差，虚线=95% 一致性界值。",
                         "Bland-Altman plot: mean vs difference; solid = mean difference, dashed = 95% limits of agreement."),
        "pca": ("PCA 得分图（PC1×PC2，标准化后），椭圆为各组均值±2SD，箭头为载荷前 5 特征。",
                "PCA score plot (PC1×PC2, standardized); ellipses = group mean±2SD; arrows = top-5 loadings."),
        "paired": ("配对前后图：每受试对象一条折线连接前后测量，星号为配对检验显著性。",
                   "Paired before-after plot: one line per subject; stars denote paired-test significance."),
        "venn": ("韦恩图展示集合交并（区域数字=元素个数，非面积比例）。",
                 "Venn diagram of set intersections (region labels = counts, not area-proportional)."),
        "cluster_heatmap": ("聚类热图：行/列按 Ward 层次聚类重排，颜色映射数值（见色条）。",
                            "Clustered heatmap: rows/columns reordered by Ward linkage; color maps values."),
    }
    zh, en = T.get(chart_type, (f"{chart_type} 图。", f"{chart_type} figure."))
    if title:
        zh_full = f"图：{zh_head}{zh}"
        en_full = f"Fig. {title}. {en}"
    else:
        zh_full = zh
        en_full = en
    return f"{zh_full}\n{en_full}"
