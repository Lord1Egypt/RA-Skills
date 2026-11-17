#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
meta_topic_eval.py — Meta-analysis 选题评估引擎（ct-literature 子模块）

消费 ct_literature 检索产出（existing_metas / primary_studies.coverage /
heterogeneity_i2_est）或用户提供的 spec JSON，执行：
  1) 早期致命缺陷门控（D1–D4，命中 CRITICAL 即 short-circuit）
  2) 六维选题评分（F1–F6，从 5 起评、须引证据）
  3) 证据纪律（integrity gate：每维分数须引 evidence）
  4) 裁决三态（Strong Accept / Accept with Revisions / Reject and Pivot）

纯 stdlib、零依赖、A 档公开、不联网。检索与覆盖度判定由 ct_literature 负责，
本模块只读证据、做评估，不重复联网。

Usage:
  # 内置健康示例
  python scripts/meta_topic_eval.py --demo --out-dir ./out
  # 内置撞车/枯竭示例（验证 early gate 直接出局）
  python scripts/meta_topic_eval.py --demo-critical --out-dir ./out
  # 评估真实 spec（由 ct_literature 检索产出填充）
  python scripts/meta_topic_eval.py --spec meta_topic_spec.json --out-dir ./out
"""
import argparse
import json
import os
import sys
from datetime import datetime

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPTS_DIR)

# ── 门控阈值（可经 CLI / spec 覆盖）─────────────────────────────────────────────
RCT_N_FLOOR = 3          # D2: 合并所需最少 RCT 数
TOTAL_N_FLOOR = 200      # D2: 合并所需最小总样本量
RECENT_META_YEARS = 2    # D1: 近 N 年内 meta 视为"已有高质重叠"


def _now_year():
    return datetime.now().year


# ── 内置示例 spec ───────────────────────────────────────────────────────────────
DEMO_SPEC = {
    "topic": "PD-1/PD-L1 inhibitors vs platinum-doublet chemotherapy in advanced NSCLC (ORR)",
    "picos": {
        "population": "advanced NSCLC, treatment-naive",
        "intervention": "PD-1/PD-L1 inhibitors (monotherapy or combination)",
        "comparator": "platinum-doublet chemotherapy",
        "outcome": "objective response rate (ORR)",
        "study_design": "RCT",
    },
    "evidence": {
        "existing_metas": [
            {"title": "Old meta 2019 on PD-1 in NSCLC", "year": 2019, "type": "meta",
             "n_studies": 6, "overlap_axes": ["population"]}
        ],
        "primary_studies": {
            "rct_count": 14,
            "total_n": 6200,
            "coverage": "healthy",
            "heterogeneity_i2_est": 0.38,
        },
        "data_accessibility": {"full_text_available": True, "grey_literature_risk": "low"},
    },
    "context": {
        "clinical_gap": "免疫联合 vs 化疗在一线 advanced NSCLC 的 ORR 净获益仍存争议，且 2024+ 新 RCT 未纳入旧 meta",
        "guideline_gap": True,
    },
}

DEMO_CRITICAL_SPEC = {
    "topic": "A over-studied topic with recent overlapping meta and depleted primary evidence",
    "picos": {
        "population": "advanced NSCLC",
        "intervention": "PD-1 inhibitor",
        "comparator": "chemotherapy",
        "outcome": "OS",
        "study_design": "RCT",
    },
    "evidence": {
        "existing_metas": [
            {"title": "2025 high-quality meta on PD-1 vs chemo OS in NSCLC", "year": 2025,
             "type": "meta", "n_studies": 18,
             "overlap_axes": ["population", "intervention", "comparator", "outcome"]},
            {"title": "2024 meta on same comparison", "year": 2024, "type": "meta",
             "n_studies": 15, "overlap_axes": ["population", "intervention", "comparator", "outcome"]},
        ],
        "primary_studies": {
            "rct_count": 2,
            "total_n": 140,
            "coverage": "critical_gap",
            "heterogeneity_i2_est": 0.72,
        },
        "data_accessibility": {"full_text_available": False, "grey_literature_risk": "high"},
    },
    "context": {"clinical_gap": "no incremental question", "guideline_gap": False},
}


# ── 早期门控 ───────────────────────────────────────────────────────────────────
def run_fatal_gate(spec, year=None, rct_floor=RCT_N_FLOOR, n_floor=TOTAL_N_FLOOR,
                   recent_years=RECENT_META_YEARS):
    """返回 (defects, has_critical)。命中 CRITICAL 即 short-circuit。"""
    year = year or _now_year()
    ev = spec.get("evidence", {})
    ps = ev.get("primary_studies", {})
    metas = ev.get("existing_metas", [])
    defects = []

    # D1 重叠撞车：近 N 年、高质、PICOS 近似（overlap 轴覆盖 ≥ 其他全部）
    core_axes = ["population", "intervention", "comparator", "outcome"]
    for m in metas:
        if m.get("year", 0) >= year - recent_years:
            ax = m.get("overlap_axes", [])
            covered = sum(1 for a in core_axes if a in ax)
            if covered >= len(core_axes):  # 全轴重叠 = 撞车
                defects.append({
                    "id": "D1", "flaw": "重叠撞车", "severity": "CRITICAL",
                    "defense": "换差异轴或缩 PICOS 做增量亚组（如仅一线 / 仅某 PD-L1 表达亚群）",
                    "detail": "近 %d 年高质 meta《%s》(%d) 已覆盖全部 PICOS 轴" %
                              (recent_years, m.get("title", ""), m.get("year", 0)),
                })
                break

    # D2 原始研究枯竭
    rct_n = ps.get("rct_count") or 0
    total_n = ps.get("total_n")           # None = 数据源不提供样本量，不武断判定
    if rct_n < rct_floor or (total_n is not None and total_n < n_floor):
        defects.append({
            "id": "D2", "flaw": "原始研究枯竭", "severity": "CRITICAL",
            "defense": "改单臂/描述性综述，或延迟至证据成熟",
            "detail": "rct_count=%s(<%d)%s -> 无法合并或功效不足" %
                      (rct_n, rct_floor,
                       "" if total_n is None
                       else " 或 total_n=%s(<%d)" % (total_n, n_floor)),
        })

    # D3 数据不可及
    da = ev.get("data_accessibility", {})
    if da.get("full_text_available") is False:
        defects.append({
            "id": "D3", "flaw": "数据不可及", "severity": "CRITICAL",
            "defense": "评估灰色文献 / 联系作者获取全文路径",
            "detail": "关键 RCT 全文不可及且无译稿",
        })

    # D4 PICOS 崩塌（仅当用户提供了部分 PICOS 但缺失关键要素时触发；
    # 完全未提供视为"待补充"，不误判为伪选题——常见于脚本自动构建的 spec 尚未填充）
    picos = spec.get("picos", {})
    provided_any = any(picos.get(k) for k in ["population", "intervention",
                                              "comparator", "outcome"])
    missing = [k for k in ["population", "intervention", "comparator", "outcome"]
               if not picos.get(k)]
    if missing and provided_any:
        defects.append({
            "id": "D4", "flaw": "PICOS 崩塌", "severity": "CRITICAL",
            "defense": "重述 PICO 转化为可操作检索策略后再评估",
            "detail": "缺失要素: %s" % ", ".join(missing),
        })

    has_critical = any(d["severity"] == "CRITICAL" for d in defects)
    return defects, has_critical


# ── 六维评分 ───────────────────────────────────────────────────────────────────
def score_dimensions(spec):
    """返回六维列表，每维 {key,label,score,evidence,lift,flag}。从 5 起评、须引证据。"""
    ev = spec.get("evidence", {})
    ps = ev.get("primary_studies", {})
    metas = ev.get("existing_metas", [])
    da = ev.get("data_accessibility", {})
    ctx = spec.get("context", {})
    picos = spec.get("picos", {})
    year = _now_year()

    dims = []

    # F1 重叠核查（区分全轴撞车 / 部分重叠 / 无重叠三态，避免"有近 2 年 meta 即判 major"的误伤）
    recent = [m for m in metas if m.get("year", 0) >= year - RECENT_META_YEARS]
    _core = ["population", "intervention", "comparator", "outcome"]
    full_overlap = [m for m in recent
                    if sum(1 for a in _core if a in m.get("overlap_axes", [])) >= len(_core)]
    if full_overlap:
        titles = "; ".join("%s(%d)" % (m.get("title", ""), m.get("year", 0)) for m in full_overlap)
        dims.append(_dim("F1", "重叠核查", 3, "近 %d 年有 %d 篇全轴重叠 meta: %s" %
                         (RECENT_META_YEARS, len(full_overlap), titles),
                         "锁定差异轴（如特定亚群 / 新终点）以拉开增量", flag="major"))
    elif recent:
        titles = "; ".join("%s(%d)" % (m.get("title", ""), m.get("year", 0)) for m in recent)
        dims.append(_dim("F1", "重叠核查", 6, "近 %d 年有 %d 篇 meta 但无全轴重叠: %s" %
                         (RECENT_META_YEARS, len(recent), titles),
                         "细化差异轴（线数/PD-L1 分层/方案）以区隔", flag="warning"))
    else:
        dims.append(_dim("F1", "重叠核查", 8, "未检索到近 %d 年重叠 meta（含 --cochrane 核查）" %
                         RECENT_META_YEARS, "可进入 PROSPERO 注册前再复核"))

    # F2 原始研究充分性
    rct_n = ps.get("rct_count") or 0
    _tn = ps.get("total_n")                 # None = 数据源不提供样本量
    total_n = _tn if _tn is not None else 0  # 打分比较用：None→0（不可得，不加分）
    tn_disp = _tn if _tn is not None else "n/a"  # 展示用：诚实标注样本量不可得
    cov = ps.get("coverage", "unknown")
    if rct_n >= 10 and total_n >= 1000 and cov == "healthy":
        s, evid = 9, "rct_count=%d, total_n=%s, coverage=%s" % (rct_n, tn_disp, cov)
    elif rct_n >= 5:
        s, evid = 7, "rct_count=%d, total_n=%s, coverage=%s" % (rct_n, tn_disp, cov)
    elif rct_n >= RCT_N_FLOOR:
        s, evid = 5, "rct_count=%d (下限), total_n=%s, coverage=%s" % (rct_n, tn_disp, cov)
    else:
        s, evid = 5, "rct_count=%d(<%d) -> 证据不足" % (rct_n, RCT_N_FLOOR)
    dims.append(_dim("F2", "原始研究充分性", s, evid, "扩大检索 / 纳入灰色文献补充"))

    # F3 PICOS 清晰度（消费 enrichment 的精度缺口：四要素齐备但线数/分层等精度缺失同样降级）
    _enrich = spec.get("enrichment", {}) or {}
    missing = [k for k in ["population", "intervention", "comparator", "outcome"] if not picos.get(k)]
    gaps = (_enrich.get("picos_parsed", {}) or {}).get("gaps", []) or []
    if missing:
        dims.append(_dim("F3", "PICOS 清晰度", 4, "缺失要素: %s" % ", ".join(missing),
                         "补全 PICO 各要素后再评", flag="major"))
    elif gaps:
        dims.append(_dim("F3", "PICOS 清晰度", 6, "四要素齐备但存在精度缺口: %s" % "; ".join(gaps[:3]),
                         "补全线数/分层等精度缺口后再定稿", flag="major"))
    else:
        dims.append(_dim("F3", "PICOS 清晰度", 8, "PICOS 四要素齐备且可操作", "维持"))

    # F4 异质性可控性（消费 enrichment 的异质性来源：来源多即需预设亚组）
    i2 = ps.get("heterogeneity_i2_est", 0.5)
    hs = _enrich.get("heterogeneity_sources", []) or []
    if hs and len(hs) >= 3:
        dims.append(_dim("F4", "异质性可控性", 5,
                         "预期 I²≈%.2f 且有 %d 类异质性来源: %s" % (i2, len(hs), "; ".join(hs[:3])),
                         "按 PD-L1/病理类型/线数预设亚组 + 随机效应模型", flag="major"))
    elif i2 <= 0.3:
        dims.append(_dim("F4", "异质性可控性", 8, "预期 I²≈%.2f（低异质）" % i2, "常规固定/随机效应"))
    elif i2 <= 0.5:
        dims.append(_dim("F4", "异质性可控性", 6, "预期 I²≈%.2f（中等）" % i2, "预设亚组/元回归计划"))
    else:
        dims.append(_dim("F4", "异质性可控性", 4, "预期 I²≈%.2f（高异质）且无分层路径" % i2,
                         "设计预设亚组 / 敏感性分析", flag="major"))

    # F5 临床与增量意义
    if ctx.get("clinical_gap") and ctx.get("guideline_gap"):
        dims.append(_dim("F5", "临床与增量意义", 8, "存在未决临床/指南缺口: %s" %
                         ctx.get("clinical_gap", ""), "明确与已有 meta 的增量声明"))
    else:
        dims.append(_dim("F5", "临床与增量意义", 5, "未陈述明确增量问题", "补充与已有 meta 的差异价值",
                         flag="major"))

    # F6 偏倚与可重复性
    risk = da.get("grey_literature_risk", "low")
    if risk == "low":
        dims.append(_dim("F6", "偏倚与可重复性", 7, "灰色文献风险低", "常规偏倚评估（漏斗图/Egger）"))
    else:
        dims.append(_dim("F6", "偏倚与可重复性", 5, "灰色文献风险: %s" % risk, "预登记检索协议 + 偏倚评估",
                         flag="warning"))

    return dims


def _dim(key, label, score, evidence, lift, flag="ok"):
    return {"key": key, "label": label, "score": score, "evidence": evidence,
            "lift": lift, "flag": flag}


# ── 证据纪律（integrity gate，[inspection]）──────────────────────────────────────
def integrity_check(dims):
    """[inspection] 每维须有 evidence；缺失则标 no_grounds。返回 needs_attention 列表。"""
    flags = []
    for d in dims:
        if not d.get("evidence"):
            d["flag"] = "no_grounds"
            d["score"] = 5
            flags.append(d["key"])
    return flags


# ── 裁决 ───────────────────────────────────────────────────────────────────────
def decide_verdict(defects, has_critical, dims):
    # Reject and Pivot 仅对应 CRITICAL 缺陷（D1-D3 撞车/枯竭/数据不可及）。
    # 无 CRITICAL 时，无论 major 数量多少，一律归 Accept with Revisions（多 major
    # 由各维度 flag 在报告中显式呈现），避免"无 CRITICAL 却显示 Reject and Pivot"
    # 的语义矛盾（端到端验证中 sglt2_fix 曾因此误显示 Reject and Pivot）。
    if has_critical:
        return "Reject and Pivot"
    majors = [d for d in dims if d["flag"] == "major"]
    if majors:
        return "Accept with Revisions"
    high = [d for d in dims if d["score"] >= 8]
    if len(high) >= 2:
        return "Strong Accept"
    return "Accept with Revisions"


def top_actions(verdict, defects, dims):
    if verdict == "Reject and Pivot":
        return [d.get("defense", "") for d in defects if d["severity"] == "CRITICAL"][:3] or \
               ["重新设计选题，避开 CRITICAL 缺陷"]
    if verdict == "Accept with Revisions":
        return [d.get("lift", "") for d in dims if d["flag"] in ("major", "warning")][:3] or \
               ["缩小 PICOS 或补证据后重评"]
    return ["注册 PROSPERO", "基于检索产出构建 PRISMA 流程图", "用 R 预估算合并效应与 I²"]


# ── 渲染 ───────────────────────────────────────────────────────────────────────
def build_report(spec, defects, has_critical, dims, integrity_flags, verdict, year):
    one_liner = spec.get("topic", "")
    return {
        "topic": one_liner,
        "evaluated_at": datetime.now().isoformat(timespec="seconds"),
        "evaluated_year": year,
        "first_impression": {"type": "Meta-analysis 选题", "one_liner": one_liner},
        "fatal_gate": {"defects": defects, "has_critical": has_critical,
                       "short_circuited": has_critical},
        "dimensions": dims,
        "integrity": {"inspection_failed_dims": integrity_flags,
                      "needs_attention": bool(integrity_flags)},
        "verdict": verdict,
        "top_actions": top_actions(verdict, defects, dims),
    }


def render_md(report):
    r = report
    L = []
    L.append("# Meta-analysis 选题评估报告\n")
    L.append("**选题**：%s\n" % r["topic"])
    L.append("**评估时间**：%s（评估基准年 %d）\n" % (r["evaluated_at"], r["evaluated_year"]))
    L.append("**裁决**：**%s**\n" % r["verdict"])

    L.append("\n## 1. 一击印象\n")
    L.append("- 类型：%s\n" % r["first_impression"]["type"])
    L.append("- 一句话：%s\n" % r["first_impression"]["one_liner"])

    L.append("\n## 2. 早期门控（Early Gate）\n")
    if r["fatal_gate"]["defects"]:
        L.append("| ID | 缺陷 | 严重度 | 防御/出路 |")
        L.append("|---|---|---|---|")
        for d in r["fatal_gate"]["defects"]:
            L.append("| %s | %s | %s | %s |" % (d["id"], d["flaw"], d["severity"], d["defense"]))
    else:
        L.append("无 CRITICAL 缺陷。\n")
    if r["fatal_gate"]["short_circuited"]:
        L.append("\n> ⚠️ 命中 CRITICAL，已 short-circuit 直接出局，跳过六维打分。\n")

    if not r["fatal_gate"]["short_circuited"]:
        L.append("\n## 3. 六维雷达\n")
        L.append("| 维度 | 分(1-10) | 证据 | 提升建议 |")
        L.append("|---|---|---|---|")
        for d in r["dimensions"]:
            L.append("| %s %s | %d | %s | %s |" %
                     (d["key"], d["label"], d["score"], d["evidence"], d["lift"]))
        if r["integrity"]["inspection_failed_dims"]:
            L.append("\n> 证据纪律：以下维度缺 evidence，已锁定 5 分并标 `no_grounds`：%s\n" %
                     ", ".join(r["integrity"]["inspection_failed_dims"]))

    L.append("\n## 4. 裁决与下一步\n")
    L.append("**%s**\n" % r["verdict"])
    for i, a in enumerate(r["top_actions"], 1):
        L.append("%d. %s\n" % (i, a))
    return "\n".join(L)


# ── HTML 渲染（标准输出：详细版评估报告）────────────────────────────────────────
_VERDICT_COLOR = {
    "Strong Accept": "#1a7f37",
    "Accept with Revisions": "#b45309",
    "Reject and Pivot": "#b91c1c",
}
_FLAG_BADGE = {
    "ok": ("#1a7f37", "#eafaf0"),
    "major": ("#b45309", "#fdf3e3"),
    "warning": ("#92400e", "#fdf3e3"),
    "no_grounds": ("#b91c1c", "#fdecec"),
}


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _score_bar(score):
    color = "#1a7f37" if score >= 8 else ("#b45309" if score >= 6 else "#b91c1c")
    return ('<div class="bar"><div class="bar-fill" style="width:%d%%;background:%s"></div>'
            '<span class="bar-num">%d</span></div>' % (score * 10, color, score))


def render_html(report, spec=None):
    """渲染详细 HTML 评估报告。spec 含 LLM 补全字段时输出详细版，否则输出骨架版。"""
    spec = spec or {}
    r = report
    v = r["verdict"]
    vc = _VERDICT_COLOR.get(v, "#374151")
    enrich = spec.get("enrichment", {}) or {}
    picos = spec.get("picos", {})
    ev = spec.get("evidence", {})
    ctx = spec.get("context", {})

    L = []
    L.append('<!DOCTYPE html>')
    L.append('<html lang="zh-CN"><head><meta charset="utf-8">')
    L.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    L.append('<title>Meta-analysis 选题评估报告 · %s</title>' % _esc(r["topic"][:40]))
    L.append('<style>')
    L.append('''
    :root{--ink:#1f2937;--muted:#6b7280;--line:#e5e7eb;--bg:#f8fafc;--card:#ffffff;
          --accent:#0f766e;--accent-bg:#f0fdfa;}
    *{box-sizing:border-box}
    body{margin:0;background:var(--bg);color:var(--ink);
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
         line-height:1.65;font-size:15px}
    .wrap{max-width:1080px;margin:0 auto;padding:32px 28px 64px}
    header.report{border-bottom:2px solid var(--line);padding-bottom:20px;margin-bottom:28px}
    header.report h1{font-size:26px;margin:0 0 8px;letter-spacing:-.3px}
    .meta{color:var(--muted);font-size:13px;display:flex;flex-wrap:wrap;gap:8px 18px}
    .meta b{color:var(--ink);font-weight:600}
    h2{font-size:19px;margin:36px 0 14px;padding-left:11px;border-left:4px solid var(--accent)}
    h3{font-size:15px;margin:22px 0 10px;color:#374151}
    .card{background:var(--card);border:1px solid var(--line);border-radius:12px;
          padding:20px 22px;margin-bottom:18px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
    .verdict{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
    .verdict .pill{font-size:19px;font-weight:700;color:#fff;background:%s;
                    padding:9px 20px;border-radius:999px;letter-spacing:.3px}
    .verdict .sub{color:var(--muted);font-size:14px;max-width:640px}
    table{width:100%%;border-collapse:collapse;font-size:13.5px;margin:8px 0}
    th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
    th{background:#f1f5f9;font-weight:600;color:#374151}
    tr:nth-child(even) td{background:#fbfdff}
    .bar{position:relative;background:#eef2f6;border-radius:999px;height:20px;min-width:120px;
         overflow:hidden;display:inline-block;vertical-align:middle}
    .bar-fill{height:100%%;border-radius:999px}
    .bar-num{position:absolute;right:8px;top:0;line-height:20px;font-size:12px;
             font-weight:700;color:#1f2937}
    .badge{display:inline-block;font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:6px}
    .grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
    .kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
    .kpi .k{font-size:12px;color:var(--muted)}
    .kpi .v{font-size:20px;font-weight:700;margin-top:2px}
    .note{background:var(--accent-bg);border-left:4px solid var(--accent);
          padding:12px 16px;border-radius:0 8px 8px 0;font-size:13.5px;margin:12px 0}
    .warn{background:#fef6e7;border-left:4px solid #d97706}
    .danger{background:#fdecec;border-left:4px solid #dc2626}
    ul{margin:8px 0;padding-left:22px}
    li{margin:5px 0}
    .src{color:var(--muted);font-size:12.5px}
    code{background:#f1f5f9;padding:1px 6px;border-radius:5px;font-size:12.5px}
    .tag{display:inline-block;background:#eef2f6;color:#475569;font-size:11.5px;
         padding:1px 8px;border-radius:5px;margin-right:6px}
    @media(max-width:760px){.grid2{grid-template-columns:1fr}}
    ''' % vc)
    L.append('</style></head><body><div class="wrap">')

    # ── 头部 ──
    L.append('<header class="report">')
    L.append('<h1>Meta-analysis 选题评估报告</h1>')
    L.append('<div class="meta">')
    L.append('<span><b>题目</b>：%s</span>' % _esc(r["topic"]))
    L.append('<span><b>评估时间</b>：%s</span>' % _esc(r["evaluated_at"]))
    L.append('<span><b>基准年</b>：%d</span>' % r["evaluated_year"])
    L.append('</div></header>')

    # ── 结论汇总 ──
    L.append('<h2>一、结论汇总</h2>')
    L.append('<div class="card verdict">')
    L.append('<span class="pill" style="background:%s">%s</span>' % (vc, _esc(v)))
    L.append('<span class="sub">%s</span>' % _esc(_verdict_summary(r, spec)))
    L.append('</div>')

    # 六维 KPI
    L.append('<div class="grid2" style="grid-template-columns:repeat(3,1fr);margin-top:14px">')
    for d in r["dimensions"]:
        L.append('<div class="kpi"><div class="k">%s %s</div><div class="v">%d<span '
                 'style="font-size:12px;color:#9ca3af">/10</span></div></div>'
                 % (_esc(d["key"]), _esc(d["label"]), d["score"]))
    L.append('</div>')

    # ── PICOS 解析（enriched）──
    pp = enrich.get("picos_parsed") if enrich else None
    if pp:
        L.append('<h2>二、选题定义与 PICOS 解析</h2>')
        L.append('<div class="card">')
        L.append('<table><tr><th style="width:120px">要素</th><th>解析结果</th>'
                 '<th style="width:80px">清晰度</th></tr>')
        for key, label, clarity in [
            ("population", "P 人群", pp.get("population_clarity", "—")),
            ("intervention", "I 干预", pp.get("intervention_clarity", "—")),
            ("comparator", "C 对照", pp.get("comparator_clarity", "—")),
            ("outcome", "O 结局", pp.get("outcome_clarity", "—")),
            ("study_design", "S 设计", "—"),
        ]:
            L.append('<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>'
                     % (label, _esc(pp.get(key, "—")), _esc(clarity)))
        L.append('</table>')
        if pp.get("gaps"):
            L.append('<div class="note warn"><b>关键缺口</b>：%s</div>'
                     % _esc("；".join(pp["gaps"])))
        L.append('</div>')
    elif picos:
        L.append('<h2>二、选题定义（PICOS）</h2><div class="card">')
        L.append('<table><tr><th style="width:120px">要素</th><th>内容</th></tr>')
        for key, label in [("population", "P 人群"), ("intervention", "I 干预"),
                           ("comparator", "C 对照"), ("outcome", "O 结局"),
                           ("study_design", "S 设计")]:
            L.append('<tr><td><b>%s</b></td><td>%s</td></tr>' % (label, _esc(picos.get(key, "—"))))
        L.append('</table></div>')

    # ── 检索策略与结果（enriched）──
    ss = enrich.get("search_strategy") if enrich else None
    vf = enrich.get("verification") if enrich else None
    if ss or vf:
        L.append('<h2>三、检索策略与真实结果</h2><div class="card">')
        if ss:
            L.append('<table>')
            L.append('<tr><th style="width:140px">数据源</th><td>%s</td></tr>'
                     % _esc(" + ".join(ss.get("sources", []))))
            L.append('<tr><th>检索式</th><td><code>%s</code></td></tr>' % _esc(ss.get("query", "")))
            L.append('<tr><th>总命中</th><td>%s</td></tr>' % _esc(ss.get("total", "—")))
            L.append('<tr><th>覆盖度</th><td>%s</td></tr>' % _esc(ss.get("coverage", "—")))
            L.append('</table>')
        if vf:
            L.append('<h3>引文验证</h3>')
            L.append('<p class="src">%s</p>' % _esc(vf.get("summary", "")))
        L.append('</div>')

    # ── 早期门控 ──
    L.append('<h2>%s、早期致命缺陷门控</h2>' % _cn_num(4 if (ss or vf) else 3 if pp or picos else 2))
    L.append('<div class="card">')
    defects = r["fatal_gate"]["defects"]
    if defects:
        L.append('<table><tr><th style="width:52px">ID</th><th style="width:110px">缺陷</th>'
                 '<th style="width:80px">严重度</th><th>说明</th></tr>')
        for d in defects:
            L.append('<tr><td><b>%s</b></td><td>%s</td><td><span class="badge" '
                     'style="color:#b91c1c;background:#fdecec">%s</span></td><td>%s</td></tr>'
                     % (_esc(d["id"]), _esc(d["flaw"]), _esc(d["severity"]), _esc(d["detail"])))
        L.append('</table>')
    else:
        L.append('<div class="note">无 CRITICAL 缺陷，未触发短路，进入六维评分。</div>')
    if r["fatal_gate"]["short_circuited"]:
        L.append('<div class="note danger"><b>已短路</b>：命中 CRITICAL，跳过六维打分。</div>')
    L.append('</div>')

    # ── 六维评估详表 ──
    if r["dimensions"]:
        L.append('<h2>%s、六维评估详表</h2>' % _cn_num(5 if (ss or vf) else 4 if pp or picos else 3))
        L.append('<div class="card">')
        L.append('<table><tr><th style="width:70px">维度</th><th style="width:120px">评分</th>'
                 '<th>证据</th><th style="width:180px">提升建议</th></tr>')
        for d in r["dimensions"]:
            fg, bg = _FLAG_BADGE.get(d["flag"], ("#374151", "#f1f5f9"))
            L.append('<tr><td><b>%s</b> %s</td><td>%s</td><td>%s</td>'
                     '<td><span class="badge" style="color:%s;background:%s">%s</span> %s</td></tr>'
                     % (_esc(d["key"]), _esc(d["label"]), _score_bar(d["score"]),
                        _esc(d["evidence"]), fg, bg, _esc(d["flag"]), _esc(d["lift"])))
        L.append('</table></div>')

    # ── F1 重叠核查详表（enriched）──
    oa = enrich.get("overlap_analysis") if enrich else None
    if oa:
        L.append('<h2>%s、F1 重叠核查：已有 Meta 逐一分析</h2>' % _cn_num(6 if (ss or vf) else 5 if pp or picos else 4))
        L.append('<div class="card">')
        L.append('<div class="note"><b>关键发现</b>：%s</div>' % _esc(enrich.get("overlap_conclusion", "")))
        L.append('<table><tr><th style="width:52px">年份</th><th>题目</th>'
                 '<th style="width:60px">被引</th><th style="width:110px">重叠判断</th></tr>')
        for m in oa:
            L.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                     % (_esc(m.get("year", "—")), _esc(m.get("title", "")),
                        _esc(m.get("cited", "—")), _esc(m.get("verdict", ""))))
        L.append('</table></div>')

    # ── F2 核心原始研究（enriched）──
    kt = enrich.get("key_trials") if enrich else None
    if kt:
        L.append('<h2>%s、F2 核心原始研究（高影响力 RCT 代理）</h2>' % _cn_num(7 if (ss or vf) else 6 if pp or picos else 5))
        L.append('<div class="card">')
        L.append('<table><tr><th style="width:52px">年份</th><th>研究</th>'
                 '<th style="width:60px">被引</th><th>定位</th></tr>')
        for t in kt:
            L.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                     % (_esc(t.get("year", "—")), _esc(t.get("title", "")),
                        _esc(t.get("cited", "—")), _esc(t.get("trial", ""))))
        L.append('</table></div>')

    # ── 临床增量分析（enriched）──
    cg = enrich.get("clinical_gap_analysis") if enrich else None
    if cg:
        L.append('<h2>%s、F5 临床与增量意义</h2>' % _cn_num(8 if (ss or vf) else 7 if pp or picos else 6))
        L.append('<div class="card"><p>%s</p></div>' % _esc(cg))

    # ── 异质性来源（enriched）──
    hs = enrich.get("heterogeneity_sources") if enrich else None
    if hs:
        L.append('<h2>%s、F4 异质性来源与分层建议</h2>' % _cn_num(9 if (ss or vf) else 8 if pp or picos else 7))
        L.append('<div class="card"><ul>')
        for h in hs:
            L.append('<li>%s</li>' % _esc(h))
        L.append('</ul></div>')

    # ── 裁决与调整建议 ──
    base = 10 if (ss or vf) else 9 if pp or picos else 8
    adj = enrich.get("adjustments") if enrich else None
    L.append('<h2>%s、裁决与调整建议</h2>' % _cn_num(base))
    L.append('<div class="card">')
    L.append('<div class="verdict" style="margin-bottom:14px">')
    L.append('<span class="pill" style="background:%s">%s</span>' % (vc, _esc(v)))
    L.append('</div>')
    if adj:
        L.append('<table><tr><th style="width:64px">优先级</th><th style="width:150px">调整项</th><th>具体动作</th></tr>')
        for a in adj:
            L.append('<tr><td><span class="badge" style="color:#fff;background:#b45309">%s</span></td>'
                     '<td>%s</td><td>%s</td></tr>'
                     % (_esc(a.get("priority", "")), _esc(a.get("item", "")), _esc(a.get("action", ""))))
        L.append('</table>')
    L.append('<h3>下一步行动</h3><ol>')
    for i, act in enumerate(r["top_actions"], 1):
        L.append('<li>%s</li>' % _esc(act))
    L.append('</ol></div>')

    # ── 数据溯源 ──
    L.append('<h2>%s、数据溯源</h2>' % _cn_num(base + 1))
    L.append('<div class="card"><p class="src">%s</p></div>'
             % _esc(enrich.get("provenance", "本报告由 ct-literature --meta-topic-eval 生成。")))

    L.append('</div></body></html>')
    return "\n".join(L)


def _cn_num(n):
    return ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
            "十一", "十二"][n] if n < 12 else str(n)


def _verdict_summary(report, spec):
    """一句话结论汇总。"""
    v = report["verdict"]
    majors = [d for d in report["dimensions"] if d["flag"] == "major"]
    if v == "Accept with Revisions":
        if majors:
            return ("证据充分、值得立项，但存在 %d 个 MAJOR 待修订（%s），"
                    "修订后可进入 PROSPERO 注册。" %
                    (len(majors), "、".join("%s %s" % (d["key"], d["label"]) for d in majors)))
        return "证据充分、值得立项，修订细节后可进入 PROSPERO 注册。"
    if v == "Strong Accept":
        return "无 CRITICAL、多维高分，可直接进入 PROSPERO 注册与方案撰写。"
    return "命中 CRITICAL 缺陷，建议重新设计选题或换差异轴后再评估。"


# ── 函数式入口（供 ct_literature 主流程直接调用，避免重复进程）──────────────────
def evaluate(spec, out_dir="./out", run=True):
    """给定 spec 执行评估并写出 JSON+MD。返回 report dict。

    供 ct_literature 主流程在检索完成后调用：先由其把检索产出结构化为 spec，
    此处只消费 spec、做门控+评分+裁决，不联网、不重复检索。
    """
    os.makedirs(out_dir, exist_ok=True)
    year = _now_year()
    defects, has_critical = run_fatal_gate(spec, year=year)
    if has_critical:
        dims = []          # short-circuit：命中 CRITICAL 不做装饰性打分
        integrity_flags = []
    else:
        dims = score_dimensions(spec)
        integrity_flags = integrity_check(dims)
    verdict = decide_verdict(defects, has_critical, dims)
    report = build_report(spec, defects, has_critical, dims, integrity_flags, verdict, year)
    json_path = os.path.join(out_dir, "meta_topic_eval.json")
    md_path = os.path.join(out_dir, "meta_topic_eval.md")
    html_path = os.path.join(out_dir, "meta_topic_eval.html")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_md(report))
    # HTML 详细报告（标准输出）：含 LLM 补全字段时为详细版，否则为骨架版
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render_html(report, spec))
        html_ok = True
    except Exception as e:  # HTML 渲染失败不阻断主流程（MD/JSON 仍是权威产物）
        html_ok = False
        print("[warn] HTML 渲染失败: %s" % e, file=sys.stderr)
    print("裁定: %s" % verdict)
    print("早期门控 CRITICAL: %s" % has_critical)
    if not has_critical:
        print("六维: " + ", ".join("%s=%d" % (d["key"], d["score"]) for d in dims))
    print("产物: %s | %s%s" % (json_path, md_path,
                               " | %s" % html_path if html_ok else ""))
    return report


# ── CLI ────────────────────────────────────────────────────────────────────────
def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="Meta-analysis 选题评估引擎（ct-literature 子模块）")
    p.add_argument("--spec", help="spec JSON 路径（由 ct_literature 检索产出填充）")
    p.add_argument("--demo", action="store_true", help="使用内置健康示例")
    p.add_argument("--demo-critical", action="store_true", help="使用内置撞车/枯竭示例")
    p.add_argument("--out-dir", default="./out", help="输出目录（默认 ./out）")
    p.add_argument("--run", action="store_true", help="显式执行（opt-in 纪律，默认仅解析）")
    args = p.parse_args(argv)

    if args.demo:
        spec = DEMO_SPEC
    elif args.demo_critical:
        spec = DEMO_CRITICAL_SPEC
    elif args.spec:
        spec = load_spec(args.spec)
    else:
        p.error("必须指定 --demo / --demo-critical / --spec")

    if not args.run:
        print("[SAFE PREVIEW] 仅解析 spec，未执行评估。加 --run 执行。")
        print(json.dumps(spec, ensure_ascii=False, indent=2)[:500])
        return 0

    evaluate(spec, out_dir=args.out_dir, run=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
