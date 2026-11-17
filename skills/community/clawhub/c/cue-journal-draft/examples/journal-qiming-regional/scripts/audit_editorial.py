#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit_editorial.py — 编辑定位门禁（内容侧）

`audit_layout.py` 管「好不好看」，`crosscheck.py` 管「一不一致」，
`build_draft.py --stats` 管「够不够长」。**没有一道管「对不对路」**——
这本刊到底写给谁、要他读完做什么、该用什么调子说。

实测（2026-09-18，某律所区域观察第 27 期，全刊 46676 字）：
  · 48 个内容单元全部同一形态，均 409 字，而 unit-patterns.md 声明 180–320（超上限 28%）
  · 全刊读者称谓仅 4 次（0.09‰）——通篇不直接对读者说话
  · 48 条中仅 10 条含行动建议（21%）
  · 句长中位 46 字，31% 超 60 字
四条全都不报错。根因是定位此前没有机器可读的载体，只有 issue-brief 里的一句散文。

本脚本读 `positioning.json`（定位卡）+ `content.json`，把定位变成六道可判的题：

    python audit_editorial.py --content content.json --positioning positioning.json
    python audit_editorial.py --content content.json --positioning positioning.json --json
    python audit_editorial.py --content content.json --positioning positioning.json --strict
    python audit_editorial.py --content content.json --no-positioning-gate   # 只查通用项

退出码：0 = 通过 / 1 = 门禁失败（FAIL，或 --strict 下有 WARN）/ 2 = 参数或文件不可用。
**定位卡缺失时报 FAIL 并 exit 1**，不假装检查过（除非显式 --no-positioning-gate）。

六题
  1 positioning   定位卡存在且完整（目的/读者/价值承诺/调性刻度）
  2 unit_length   单条字数落在调性密度派生的区间内（越界 >30% 判 FAIL）
  3 reader_action 兑现「读者读完要做什么」的条数覆盖率（<50% 判 FAIL）
  4 l0_ratio      纯 L0（既无影响判断也无行动）条目占比（>50% 判 FAIL，硬规则 30）
  5 sentence_len  句长中位 vs 密度刻度允许的上限
  6 jargon        术语密度 vs jargon_ceiling，以及行业忌讳词命中（命中即 FAIL）
"""
from __future__ import print_function

import argparse
import json
import os
import re
import sys

# ── 词表 ────────────────────────────────────────────────────────────
ACTION_W = ["建议", "应当", "应尽快", "需注意", "可考虑", "尽快", "务必",
            "下一步", "行动", "我们建议", "请核对", "应于", "需在"]
IMPACT_W = ["意味", "影响", "意味着", "将导致", "风险", "机会", "挑战",
            "利好", "改变了", "首次", "标志着", "使得", "由此"]
READER_W = ["您", "贵司", "贵公司", "贵行", "贵校", "企业可", "你可", "对你"]

# 密度刻度 → 单条字数带 / 句长上限（见 references/audience-value.md §四）
DENSITY_SCALE = {
    1: (60, 120, 20),
    2: (120, 200, 30),
    3: (200, 320, 40),
    4: (320, 600, 50),
    5: (600, 1200, 60),
}

SPLIT = re.compile(r"[。！？；\n]")
LATIN = re.compile(r"[A-Za-z][A-Za-z\-]{1,}")


def txt(o):
    """递归取文本。"""
    if isinstance(o, dict):
        return " ".join(txt(v) for v in o.values())
    if isinstance(o, list):
        return " ".join(txt(v) for v in o)
    return o if isinstance(o, str) else ""


def plain(s):
    return re.sub(r"\s", "", s or "")


def content_blocks(content):
    """拆成内容块：unit_list 页按条，其余页按 fields 的字段。

    只保留 ≥15 字的块——封面期号、页眉页脚这类固定件不参与编辑质量判定。
    """
    out = []
    for pg in (content.get("pages") or []):
        tpl = pg.get("template") or ""
        if tpl == "unit_list":
            for u in pg.get("units") or []:
                s = txt(u)
                if len(plain(s)) >= 15:
                    out.append(("unit", s))
        else:
            for k, v in (pg.get("fields") or {}).items():
                s = txt(v)
                if len(plain(s)) >= 15:
                    out.append(("field:" + tpl, s))
    return out


def implied_blocks(content):
    """参与「读者价值兑现」判定的块 = unit_list 的条（正文条目的主体）。"""
    out = []
    for pg in (content.get("pages") or []):
        if (pg.get("template") or "") == "unit_list":
            for u in pg.get("units") or []:
                s = txt(u)
                if len(plain(s)) >= 15:
                    out.append(s)
    return out


def derive_tone(tone):
    """由 density 刻度派生字数带与句长上限；定位卡里手写的优先。"""
    try:
        d = int((tone or {}).get("density", 3))
    except (TypeError, ValueError):
        d = 3
    lo, hi, smax = DENSITY_SCALE.get(max(1, min(5, d)), DENSITY_SCALE[3])
    dv = (tone or {}).get("derived") or {}
    try:
        lo = int(dv.get("unit_chars_min", lo))
        hi = int(dv.get("unit_chars_max", hi))
    except (TypeError, ValueError):
        pass
    try:
        smax = int(dv.get("sentence_len_median_max", smax))
    except (TypeError, ValueError):
        pass
    if hi <= lo:
        hi = lo + 50
    return lo, hi, smax


def main():
    ap = argparse.ArgumentParser(description="编辑定位门禁（内容侧）")
    ap.add_argument("--content", required=True, help="content.json")
    ap.add_argument("--positioning", help="positioning.json（定位卡）")
    ap.add_argument("--no-positioning-gate", action="store_true",
                    help="没有定位卡时不判 FAIL，只查通用项")
    ap.add_argument("--strict", action="store_true", help="WARN 也算失败")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args()

    if not os.path.isfile(a.content):
        sys.stderr.write("[ERR] 找不到 content: %s\n" % a.content)
        return 2
    try:
        content = json.load(open(a.content, encoding="utf-8"))
    except Exception as e:
        sys.stderr.write("[ERR] content 解析失败: %s\n" % e)
        return 2

    pos = None
    pos_path = a.positioning
    if pos_path and os.path.isfile(pos_path):
        try:
            pos = json.load(open(pos_path, encoding="utf-8"))
        except Exception as e:
            sys.stderr.write("[ERR] positioning 解析失败: %s\n" % e)
            return 2

    checks = []
    metrics = {}

    def add(name, level, msg, detail=""):
        checks.append({"name": name, "level": level, "msg": msg, "detail": detail})

    blocks = content_blocks(content)
    units = implied_blocks(content)
    full = txt(content)
    pfull = plain(full)
    n_all = len(pfull) or 1
    metrics["blocks"] = len(blocks)
    metrics["units"] = len(units)
    metrics["chars_total"] = len(pfull)

    # ── 1. 定位卡 ────────────────────────────────────────────────────
    if pos is None:
        if a.no_positioning_gate:
            add("positioning", "WARN", "无定位卡（已显式跳过），只查通用项", "")
        else:
            add("positioning", "FAIL", "缺 positioning.json —— 定位没落成产物",
                "先按 assets/templates/positioning.template.json 填一份；"
                "口径见 references/audience-value.md。不填就无法判断这本刊对不对路")
    else:
        miss = [k for k in ("purpose", "audience", "value_promise", "tone")
                if not (pos.get(k) or {}).items()]
        prim = ((pos.get("purpose") or {}).get("primary") or "").strip().upper()
        bad = []
        if "purpose" in miss:
            bad.append("purpose")
        elif prim not in ("A", "B", "C", "D", "E", "F"):
            bad.append("purpose.primary 不是 A–F（值为 %r）" % prim)
        if "audience" in miss:
            bad.append("audience")
        elif not (pos.get("audience") or {}).get("role"):
            bad.append("audience.role 为空（不要写『客户』这类词，追到岗位）")
        if "value_promise" in miss:
            bad.append("value_promise")
        elif not (pos.get("value_promise") or {}).get("reader_action"):
            bad.append("value_promise.reader_action 为空（必须是一个动词短语）")
        if "tone" in miss:
            bad.append("tone")
        if bad:
            add("positioning", "FAIL", "定位卡不完整：%s" % "；".join(bad), "")
        else:
            add("positioning", "OK",
                "定位卡完整：目的 %s / 读者 %s / 调性 权威%s·密度%s·立场%s"
                % (prim, (pos.get("audience") or {}).get("role", "?")[:12],
                   (pos.get("tone") or {}).get("authority"),
                   (pos.get("tone") or {}).get("density"),
                   (pos.get("tone") or {}).get("stance")), "")

    lo, hi, smax = derive_tone((pos or {}).get("tone"))
    metrics["unit_chars_range"] = [lo, hi]
    metrics["sentence_len_max"] = smax

    # ── 2. 单条字数带 ────────────────────────────────────────────────
    if units:
        lens = [len(plain(s)) for s in units]
        avg = sum(lens) / float(len(lens))
        over = [x for x in lens if x > hi]
        under = [x for x in lens if x < lo]
        ratio = len(over) / float(len(lens))
        metrics["unit_chars_avg"] = round(avg, 1)
        metrics["unit_over_ratio"] = round(ratio, 3)
        metrics["unit_over"] = len(over)
        metrics["unit_under"] = len(under)
        if ratio > 0.30:
            add("unit_length", "FAIL",
                "单条均 %.0f 字，%d/%d 条（%.0f%%）超出 %d–%d 字带"
                % (avg, len(over), len(lens), ratio * 100, lo, hi),
                "密度刻度与字数带不匹配。改法：降 density 刻度并压字数，"
                "不是把条目灌长——灌长后信息密度反而更低（硬规则 17）")
        elif ratio > 0.10:
            add("unit_length", "WARN",
                "单条均 %.0f 字，%d/%d 条（%.0f%%）超出 %d–%d 字带"
                % (avg, len(over), len(lens), ratio * 100, lo, hi), "")
        else:
            add("unit_length", "OK", "单条均 %.0f 字，落在 %d–%d 字带内" % (avg, lo, hi), "")
    else:
        add("unit_length", "WARN", "没有 unit_list 条目，跳过", "")

    # ── 3. 读者动作兑现率 ────────────────────────────────────────────
    if units:
        act = sum(1 for s in units
                  if any(w in s for w in ACTION_W)
                  or any(w in s for w in READER_W))
        cov = act / float(len(units))
        metrics["reader_action_cov"] = round(cov, 3)
        if cov < 0.50:
            add("reader_action", "FAIL",
                "兑现『读者要做什么』的条目 %d/%d（%.0f%%），低于 50%%"
                % (act, len(units), cov * 100),
                "value_promise.reader_action 写了却没有内容兑现＝定位空转。"
                "改法：每条补一句动作（建议/应于/请核对），不是加长背景")
        elif cov < 0.70:
            add("reader_action", "WARN",
                "兑现『读者要做什么』的条目 %d/%d（%.0f%%）" % (act, len(units), cov * 100), "")
        else:
            add("reader_action", "OK",
                "兑现『读者要做什么』的条目 %d/%d（%.0f%%）" % (act, len(units), cov * 100), "")
    else:
        add("reader_action", "WARN", "没有 unit_list 条目，跳过", "")

    # ── 4. 纯 L0 占比（硬规则 30）────────────────────────────────────
    if units:
        l0 = sum(1 for s in units
                 if not any(re.search(w, s) for w in IMPACT_W)
                 and not any(w in s for w in ACTION_W))
        r = l0 / float(len(units))
        metrics["l0_ratio"] = round(r, 3)
        if r > 0.50:
            add("l0_ratio", "FAIL",
                "纯 L0 条目 %d/%d（%.0f%%），超过一半 —— 这是信息堆叠"
                % (l0, len(units), r * 100),
                "硬规则 30：每条至少一句 L1（点名受影响的主体与环节）。"
                "判据：遮掉机构名还看得出是谁写的吗？")
        elif r > 0.30:
            add("l0_ratio", "WARN", "纯 L0 条目 %d/%d（%.0f%%）" % (l0, len(units), r * 100), "")
        else:
            add("l0_ratio", "OK", "纯 L0 条目 %d/%d（%.0f%%）" % (l0, len(units), r * 100), "")

    # ── 5. 句长 ──────────────────────────────────────────────────────
    sents = [s for s in SPLIT.split(full) if len(plain(s)) > 2]
    if sents:
        L = sorted(len(plain(s)) for s in sents)
        med = L[len(L) // 2]
        long_r = sum(1 for x in L if x > 60) / float(len(L))
        metrics["sentence_median"] = med
        metrics["long_sentence_ratio"] = round(long_r, 3)
        if med > smax:
            add("sentence_len", "WARN",
                "句长中位 %d 字，超过密度刻度允许的 %d 字；超 60 字的长句占 %.0f%%"
                % (med, smax, long_r * 100),
                "读者时间预算被无视的典型症状。改法：拆句，不是删内容")
        else:
            add("sentence_len", "OK",
                "句长中位 %d 字（上限 %d），超 60 字长句占 %.0f%%"
                % (med, smax, long_r * 100), "")

    # 读者称谓密度
    rd = sum(full.count(w) for w in READER_W)
    metrics["reader_terms_per_1k"] = round(rd / float(n_all) * 1000, 3)
    sp = (((pos or {}).get("tone") or {}).get("derived") or {}).get("second_person", "optional")
    if sp == "required" and rd == 0:
        add("reader_terms", "FAIL", "调性要求第二人称，全文 0 次",
            "读者定位要求直接对话，但通篇第三人称＝不对读者说话")
    elif sp == "forbidden" and rd > 0:
        add("reader_terms", "WARN", "调性禁用第二人称，出现 %d 次" % rd, "")
    else:
        # 有主张（立场 >=4）却几乎不对读者说话＝把判断写成旁观者的旁白
        stance = ((pos or {}).get("tone") or {}).get("stance")
        per1k_rd = rd / float(n_all) * 1000
        try:
            hi_stance = stance is not None and int(stance) >= 4
        except (TypeError, ValueError):
            hi_stance = False
        if hi_stance and per1k_rd < 0.5:
            add("reader_terms", "WARN",
                "读者称谓仅 %d 次（%.2f/千字）——立场 %s 却通篇不对读者说话"
                % (rd, per1k_rd, stance),
                "判断要落到读者身上才有价值。改法：把「企业应当…」改成「贵司需在…」，"
                "不是加长论述")
        else:
            add("reader_terms", "OK",
                "读者称谓 %d 次（%.2f/千字）" % (rd, per1k_rd), "")

    # ── 6. 术语与忌讳词 ──────────────────────────────────────────────
    irules = (pos or {}).get("industry_rules") or {}
    taboo = irules.get("taboo_words") or []
    hits = []
    for w in taboo:
        w = (w or "").strip()
        if w and w in full:
            hits.append((w, full.count(w)))
    metrics["taboo_hits"] = hits
    if hits:
        add("jargon", "FAIL",
            "命中行业忌讳词 %s" % "、".join("%s×%d" % (w, c) for w, c in hits),
            "这些词即便合规也应避开（见 audience-value.md §五）")
    else:
        extra = irules.get("jargon_terms") or []
        jargon_n = len(LATIN.findall(full)) + sum(full.count(w) for w in extra)
        per1k = jargon_n / float(n_all) * 1000
        metrics["jargon_per_1k"] = round(per1k, 2)
        ceiling = irules.get("jargon_ceiling_per_1k")
        if ceiling is not None:
            try:
                if per1k > float(ceiling) * 1.25:
                    add("jargon", "WARN",
                        "术语密度 %.1f/千字，超出 ceiling %.0f 的 25%%"
                        % (per1k, float(ceiling)),
                        "专业水平被高估：要么降 jargon_ceiling，要么首次出现就解释")
                else:
                    add("jargon", "OK", "术语密度 %.1f/千字（ceiling %.0f），无忌讳词"
                        % (per1k, float(ceiling)), "")
            except (TypeError, ValueError):
                add("jargon", "OK", "无忌讳词命中", "")
        else:
            add("jargon", "OK", "无忌讳词命中（未设 jargon_ceiling，术语密度 %.1f/千字）"
                % per1k, "")

    # ── 输出 ─────────────────────────────────────────────────────────
    n_fail = sum(1 for c in checks if c["level"] == "FAIL")
    n_warn = sum(1 for c in checks if c["level"] == "WARN")

    if a.json:
        print(json.dumps({"content": a.content, "positioning": pos_path,
                          "metrics": metrics, "checks": checks,
                          "fail": n_fail, "warn": n_warn},
                         ensure_ascii=False, indent=1))
    else:
        print("编辑定位门禁 — %s" % os.path.basename(a.content))
        print("  单元 %d 条 / 内容块 %d / 全刊 %d 字" % (len(units), len(blocks), len(pfull)))
        for c in checks:
            tag = {"OK": "[ OK ]", "WARN": "[WARN]", "FAIL": "[FAIL]"}[c["level"]]
            print("  %s %-14s %s" % (tag, c["name"], c["msg"]))
            if c["detail"] and c["level"] != "OK":
                print("         └─ %s" % c["detail"])
        print("  ── FAIL %d / WARN %d" % (n_fail, n_warn))
        if n_fail == 0 and n_warn == 0:
            print("  编辑定位门禁通过。")
        elif n_fail == 0:
            print("  无阻塞项；WARN 建议逐条看一眼再交付。")

    return 1 if (n_fail or (a.strict and n_warn)) else 0


if __name__ == "__main__":
    sys.exit(main())
