#!/usr/bin/env python3
"""ct-literature → self-contained HTML report (no Excel needed to view).

Reads `.merged.json` (OpenAlex + Europe PMC merged evidence base) and renders a
single standalone .html file (inline CSS, safety-row highlight, source/type
distributions as CSS bars) so content is fully readable in any browser / the
WorkBuddy artifact preview without the client's limited xlsx viewer.

Theme: literature academic green, reusing vendored excel_style palette.

Usage:
    python export_html.py --in-json ../out_live/.merged.json \
                          --out ../out_live/lit_report.html --lang zh
"""
import os, sys, json, html, argparse, datetime, itertools, math, os.path, re, ast
from collections import Counter

# IMPORTANT (2026-08-11): ct-base is NEVER published. Every ct- skill must carry
# its own complete copy. We ONLY import from this skill's own `scripts/` dir.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import excel_style as X
from export_xlsx import restore_abstract_paragraphs
from xlsx_delivery import resolve_report_lang  # ct-base 共享件

# §22 governance sections (ct-base §22.16 / §22.17) — shared with report.py.
try:
    from gov22 import build_gov22
except ImportError:  # pragma: no cover
    build_gov22 = None

PALETTE = X.PALETTES["literature"]

_LABELS = {
    "en": {
        "doc_title": "Literature Evidence Base",
        "generated": "Generated", "kpi.total": "Works", "kpi.safety": "Safety-related",
        "search.topic": "Search Topic", "search.keywords": "Generated Keywords",
        "search.filter": "Filter", "search.none": "—",
        "kpi.year": "Year Span", "kpi.topcited": "Top Cited",
        "works": "Works", "col.source": "Source", "col.id": "ID", "col.srcid": "Source / ID", "col.title": "Title",
        "col.authors": "Authors", "col.year": "Year", "col.pub": "Publication",
        "col.type": "Type", "col.study": "Study", "col.cited": "Cited", "col.relevance": "Relevance", "col.relevance_basis": "Relevance basis", "col.link": "Link",
        "col.oa": "Open Access",
        "col.pdf": "PDF",
        "col.abstract": "Abstract", "overview": "Overview", "by_src": "By Source",
        "rel.overview": "Relevance overview (machine-assisted sort)",
        "rel.overview.note": "Based on your query; sort/prompt only, NOT a final include/exclude screening decision.",
        "rel.band": "Relevance band", "rel.share": "Share",
        "rel.high": "High (>=0.5)", "rel.mid": "Medium (0.2-0.5)", "rel.low": "Low (<0.2)",
        "by_type": "By Type", "by_year": "By Year", "safety": "Safety / CSM Subset",
        "abs.more": "Show full abstract ▾", "abs.less": "Collapse ▴",
        "tips.title": "Need more? / Options",
        "tips.t1": "Excel workbook is the complete result — keep analysing / filtering it on top.",
        "tips.t2": "PDF downloads on request — ALL OA records, specific DOI / PMID(s), or the top N (legal OA sources only).",
        "tips.t3": "Citation formats (Zotero RIS / BibTeX / APA …) can be generated for download on request.",
        "tips.t4": "Not sure about an add-on? Say “menu” in the chat and I will walk you through the choices.",
        "evidence": "Evidence & Verification", "ev.verify": "Citation verification",
        "ev.verified": "Verified", "ev.bot_blocked": "Bot-blocked",
        "ev.bot_blocked.note": "publisher returned 403 to automated access — DOI is real, not a broken link",
        "ev.unresolved": "Unresolved",
        "ev.no_id": "No identifier", "ev.suspicious": "Suspicious",
        "ev.mismatch": "Mismatch",
        "ev.mismatch.note": "identifier resolved to a LIVE resource but title/author do NOT match — possible hallucinated/incorrect id",
        "src.banner": "🔎 Source: ct-literature (local + Coze dual-engine; OpenAlex primary)",
        "cite.foot": "⚠️ Citation count reflects impact, NOT evidence quality; clinical evidence grade follows study design (RCT / systematic review).",
        "preprint.tag": "⚠️ preprint · not peer-reviewed",
        "ev.src_summary": "Source status",
        "cfg.warn": ("OpenAlex API key not configured — this run used the keyless pool "
                     "(100 credits/day, easily rate-limited). Apply for a FREE key and write it "
                     "to the skill `.env` as `OPENALEX_API_KEY=<key>`, then re-run for full coverage:"),
        "ev.preview": "preview — skipped", "ev.src": "Source", "ev.query": "Query",
        "ev.type": "Type", "ev.year": "Year", "ev.safety": "Safety",
        "ev.count": "Count", "ev.retrieved": "Retrieved", "ev.status": "Status",
        "net.title": "Concept Co-occurrence Network",
        "net.note": ("Node = keyword / concept (size = co-occurrence degree, top 25); "
                     "edge = two terms co-occurring in >= 2 works (thicker = more). "
                     "Deterministic circular layout — shows co-occurrence only, "
                     "NOT a true clustering."),
        "net.legend": "Co-occurrence",
        "merge.title": "Living-review Delta",
        "merge.new": "New", "merge.carry": "Carryover", "merge.retained": "Retained",
    },
    "zh": {
        "doc_title": "文献证据库",
        "generated": "生成时间", "kpi.total": "文献数", "kpi.safety": "安全性相关",
        "search.topic": "检索主题", "search.keywords": "生成关键字",
        "search.filter": "筛选条件", "search.none": "—",
        "kpi.year": "年份跨度", "kpi.topcited": "最高被引",
        "works": "文献列表", "col.source": "来源", "col.id": "ID", "col.srcid": "来源 / ID", "col.title": "标题",
        "col.authors": "作者", "col.year": "年份", "col.pub": "期刊",
        "col.type": "类型", "col.study": "研究类型", "col.cited": "被引", "col.relevance": "相关性", "col.relevance_basis": "相关性依据", "col.link": "链接",
        "col.oa": "OA链接",
        "col.pdf": "PDF",
        "col.abstract": "摘要", "overview": "概览", "by_src": "按来源", "by_type": "按类型",
        "rel.overview": "相关性概览（机器辅助排序）",
        "rel.overview.note": "基于你的检索式；仅作排序与提示，不构成最终纳入/排除裁决。",
        "rel.band": "相关性区间", "rel.share": "占比",
        "rel.high": "高 (≥0.5)", "rel.mid": "中 (0.2–0.5)", "rel.low": "低 (<0.2)",
        "by_year": "按年份", "safety": "安全性 / CSM 子集",
        "abs.more": "点击展开全部摘要 ▾", "abs.less": "收起 ▴",
        "tips.title": "还能做什么？",
        "tips.t1": "Excel 报告是完整结果（全部记录 + 全字段），可在此基础上继续筛选 / 透视等进一步处理。",
        "tips.t2": "需要 PDF？可协助下载：全部 OA 记录、指定 DOI/PMID、或前 N 篇（仅从合法 OA 源尝试）。",
        "tips.t3": "可按需生成并下载 Zotero(RIS) / BibTeX / APA 等引文格式。",
        "tips.t4": "不确定如何选用附加功能？对话中呼叫「菜单」，我列出选项供你选择。",
        "evidence": "证据溯源与引文验证", "ev.verify": "引文验证",
        "ev.verified": "已验证", "ev.bot_blocked": "出版社拦爬",
        "ev.bot_blocked.note": "出版社对自动化访问回 403 —— DOI 真实有效、非断链",
        "ev.unresolved": "未解析",
        "ev.no_id": "无标识", "ev.suspicious": "可疑",
        "ev.mismatch": "不一致",
        "ev.mismatch.note": "标识符解析到存活资源，但标题/作者不一致 —— 可能为幻觉或错误 id",
        "src.banner": "🔎 检索来源：ct-literature（本地 + Coze 双引擎；OpenAlex 为主源）",
        "cite.foot": "⚠️ 被引次数仅反映影响力，非证据质量；临床证据等级以研究设计（RCT / 系统评价）为准。",
        "preprint.tag": "⚠️ 预印本·未经同行评审",
        "ev.src_summary": "数据源状态",
        "cfg.warn": ("未配置 OpenAlex API key —— 本次以 keyless 模式运行（限 100 次/天，易触发 429 限流）。"
                     "建议免费申请 key 并写入技能目录 `.env`（`OPENALEX_API_KEY=<key>`）后重跑以获得完整覆盖："),
        "ev.preview": "预览，已跳过", "ev.src": "来源", "ev.query": "检索式",
        "ev.type": "类型", "ev.year": "年份", "ev.safety": "安全性",
        "ev.count": "数量", "ev.retrieved": "检索时间", "ev.status": "状态",
        "net.title": "概念共现网络",
        "net.note": ("节点 = 关键词 / 概念（大小 = 共现度，取前 25）；边 = 两个词在同一文献中"
                     "共现 ≥ 2 次（越粗共现越多）。环形布局为确定性排布，仅表示共现，"
                     "不代表真实聚类。"),
        "net.legend": "共现",
        "merge.title": "增量合并",
        "merge.new": "新增", "merge.carry": "沿用", "merge.retained": "历史保留",
    },
}


def esc(v):
    return html.escape("" if v is None else str(v))


def _short_id(v):
    """Shorten a record id for the merged source·id cell: strip the scheme +
    host so 'https://openalex.org/W3087210493' -> 'W3087210493' and a DOI URL
    keeps its '10.xxxx/...' form; numeric/plain ids pass through."""
    if not v:
        return "—"
    s = str(v).strip().rstrip("/")
    m = re.match(r"^https?://[^/]+/(.*)$", s)
    return m.group(1) if m else s


def _fmt_authors(v, max_n=4):
    """Authors arrive as a list (or its repr / JSON string). Parse and render
    as 'A, B, C et al.'; max_n=0/None returns the full list for tooltips."""
    if not v:
        return "—"
    if isinstance(v, str):
        s = v.strip()
        if s.startswith("["):
            try:
                v = ast.literal_eval(s)
            except Exception:
                try:
                    v = json.loads(s)
                except Exception:
                    return s
    if isinstance(v, (list, tuple)):
        names = [str(x) for x in v if str(x).strip()]
        if not names:
            return "—"
        if max_n and len(names) > max_n:
            return ", ".join(names[:max_n]) + " et al."
        return ", ".join(names)
    return str(v)


def _html_link(u):
    """Normalise a link target: keep http(s)/ftp/mailto, prefix bare DOIs with
    https://doi.org/, and return '' for anything non-linkable (so we render '—'
    instead of a broken href)."""
    if not u:
        return ""
    u = str(u).strip()
    if u.startswith(("http://", "https://", "ftp://", "mailto:")):
        return u
    if u.startswith("10."):
        return "https://doi.org/" + u
    return ""


def bar(value, maxv, color):
    v = float(value or 0)
    pct = max(0, min(100, v / maxv * 100)) if maxv else 0
    return (f'<div class="barwrap"><div class="bar" style="width:{pct:.1f}%;'
            f'background:{color};"></div><span class="barval">{v:.0f}</span></div>')


def _sanitize(data):
    """Reuse the xlsx exporter's type-normalisation so both stay in sync."""
    try:
        import export_xlsx
        return export_xlsx.sanitize(data)
    except Exception:
        # Minimal inline fallback if the xlsx exporter is unavailable.
        works = [w for w in (data.get("works") or []) if isinstance(w, dict)]
        out = []
        for w in works:
            w = dict(w)
            y = w.get("year")
            w["year"] = y if isinstance(y, int) and not isinstance(y, bool) else (
                int(y) if isinstance(y, str) and y.strip().isdigit() else None)
            c = w.get("cited_by_count")
            w["cited_by_count"] = c if isinstance(c, int) else 0
            out.append(w)
        data = dict(data)
        data["works"] = out
        return data


def prisma_funnel_svg(prisma, P):
    """Inline SVG PRISMA-2020 funnel (no third-party deps). Returns '' if empty."""
    stages = (prisma or {}).get("stages") or []
    if not stages:
        return ""
    maxc = max((s.get("count") or 0) for s in stages) or 1
    W, H, pad, top = 620, 340, 24, 18
    n = len(stages)
    band_h = (H - top - 24) / n
    colors = [P["navy"], P["blue"], P["banner"], P["warn_bd"]]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="100%" role="img" aria-label="PRISMA funnel">']
    for i, s in enumerate(stages):
        c = s.get("count") or 0
        w = max(50, c / maxc * (W - 2 * pad))
        x = (W - w) / 2.0
        y = top + i * band_h
        col = colors[i % len(colors)]
        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{band_h - 6:.1f}" '
                   f'rx="6" fill="{col}" opacity="0.88"/>')
        cx = W / 2.0
        cy = y + (band_h - 6) / 2.0
        label = (s.get("label") or s.get("stage") or "")
        if len(label) > 42:
            label = label[:40] + "…"
        svg.append(f'<text x="{cx:.1f}" y="{cy - 2:.1f}" fill="#fff" font-size="13" '
                   f'text-anchor="middle" font-family="sans-serif">{esc(label)}</text>')
        svg.append(f'<text x="{cx:.1f}" y="{cy + 15:.1f}" fill="#fff" font-size="15" '
                   f'font-weight="700" text-anchor="middle" font-family="sans-serif">n = {c}</text>')
    svg.append('</svg>')
    return "".join(svg)


def _work_terms(w):
    """Terms of one work: keywords + concepts, de-duplicated (case-insensitive).

    Concepts may arrive as plain strings or as OpenAlex-style dicts
    ({"display_name": ...}); export_xlsx.sanitize() may already have stringified
    them, so both shapes are handled.
    """
    raw = []
    for fld in ("keywords", "concepts"):
        for c in (w.get(fld) or []):
            if isinstance(c, dict):
                t = c.get("display_name") or c.get("name") or c.get("keyword") or ""
            else:
                t = c
            t = str(t or "").strip()
            if t:
                raw.append(t)
    seen, out = set(), []
    for t in raw:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def concept_network_svg(works, P, top_n=25, min_edge=2):
    """Inline SVG concept co-occurrence network (stdlib only). Returns '' if too sparse.

    Deterministic by construction: nodes are ranked by (-degree, -frequency, term) and
    laid out on a circle from a fixed start angle — the same input set always yields a
    byte-identical SVG regardless of work ordering, so a living-review re-run does not
    produce report diff noise.

    Guards against SVG blow-up: at most `top_n` nodes and only edges with weight >=
    `min_edge` are drawn; a work contributes a pair only once even if it repeats terms.
    """
    docs = []
    for w in (works or []):
        if not isinstance(w, dict):
            continue
        ts = _work_terms(w)
        if len(ts) >= 2:
            docs.append(ts)
    if not docs:
        return ""

    freq, pairs, forms = Counter(), Counter(), {}
    for ts in docs:
        freq.update(ts)
        for t in ts:
            forms.setdefault(t.lower(), Counter())[t] += 1
        for a, b in itertools.combinations(sorted(ts), 2):
            pairs[(a, b)] += 1
    # Sorted, not just filtered: Counter preserves insertion order, which would leak
    # the work ordering into the SVG string and produce report diff noise between runs.
    # Ascending weight also paints heavy edges last (on top of the light ones).
    edges = sorted(((a, b, c) for (a, b), c in pairs.items() if c >= min_edge),
                   key=lambda e: (e[2], e[0], e[1]))
    if not edges:
        return ""
    # display form per canonical (lower-cased) key: most frequent spelling wins, ties
    # broken lexicographically -> stable under input reordering.
    disp = {k: min(c.items(), key=lambda kv: (-kv[1], kv[0]))[0] for k, c in forms.items()}

    deg = Counter()
    for a, b, _c in edges:
        deg[a] += 1
        deg[b] += 1
    nodes = sorted(deg, key=lambda t: (-deg[t], -freq.get(t, 0), t))[:max(1, top_n)]
    keep = set(nodes)
    edges = [(a, b, c) for (a, b, c) in edges if a in keep and b in keep]
    if not edges or len(nodes) < 2:
        return ""

    W, H = 760, 520
    cx, cy, R = W / 2.0, 244.0, 180.0
    n = len(nodes)
    maxdeg = max(deg.values()) or 1
    maxw = max(c for _a, _b, c in edges) or 1
    pos = {}
    for i, t in enumerate(nodes):
        ang = -math.pi / 2 + 2 * math.pi * i / n   # deterministic: start at 12 o'clock
        pos[t] = (cx + R * math.cos(ang), cy + R * math.sin(ang), ang)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="100%" role="img" aria-label="Concept co-occurrence network">',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>']
    # edges first so nodes paint on top
    for a, b, c in edges:
        x1, y1, _ = pos[a]
        x2, y2, _ = pos[b]
        w_ratio = c / float(maxw)
        svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="{P["blue"]}" stroke-width="{0.8 + 2.6 * w_ratio:.2f}" '
                   f'stroke-opacity="{0.16 + 0.44 * w_ratio:.2f}"/>')
    for t in nodes:
        x, y, ang = pos[t]
        r = 7.0 + 13.0 * math.sqrt(deg[t] / float(maxdeg))
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{P["navy"]}" '
                   f'fill-opacity="0.88" stroke="#ffffff" stroke-width="1.5"/>')
        label = disp.get(t.lower(), t)
        if len(label) > 14:
            label = label[:13] + "\u2026"
        lx = x + (r + 11) * math.cos(ang)
        ly = y + (r + 11) * math.sin(ang)
        if abs(math.cos(ang)) < 0.30:
            anchor = "middle"
        else:
            anchor = "start" if math.cos(ang) > 0 else "end"
        svg.append(f'<text x="{lx:.1f}" y="{ly + 3.5:.1f}" text-anchor="{anchor}" '
                   f'font-size="10.5" font-family="sans-serif" '
                   f'fill="{P["greytx"]}">{esc(label)}</text>')
    svg.append(f'<text x="{W / 2.0:.0f}" y="{H - 12}" text-anchor="middle" font-size="11" '
               f'font-family="sans-serif" fill="{P["greytx"]}">'
               f'nodes={len(nodes)} · edges={len(edges)} · top_n={top_n} '
               f'· min_edge={min_edge}</text>')
    svg.append('</svg>')
    return "".join(svg)




def _gov22_html(data, lang):
    """§22 governance section (ct-base §22.16 RAG checklist + §22.17 stratified
    acceptance) as HTML. Mirrors report.py's _gov22_md via the shared
    gov22.build_gov22 so Markdown and HTML stay in lock-step."""
    if build_gov22 is None:
        return ""
    works = data.get("works") or []
    meta = data.get("meta") or {}
    evidence_log = data.get("evidence_log") or {}
    g = build_gov22(works, evidence_log, meta, lang)
    zh = (lang in ("zh", "zh-CN", "zh-cn"))
    T = {
        "zh": {
            "title": "AI 生成资产治理（ct-base §22）",
            "intro": "本技能受 ct-base §22 约束。文献检索/综合输出属 RAG 类：结论绝不脱离出处交付；"
                     "「未覆盖项」须显式列出，而非假设检索完整（§22.16 + §17.1）。",
            "s16": "§22.16 RAG 三列待核对清单（问题 / 原文位置 / 依据）",
            "s16note": "默认失败模式 = 漏项。每条结论均可回溯至原文位置与依据；专业人员按清单回看原文，AI 不替人下最终结论。",
            "q": "问题", "loc": "原文位置", "basis": "依据", "cov": "是否覆盖",
            "yes": "✅ 已覆盖", "no": "⚠️ 未覆盖",
            "unc": "§22.16 显式「未覆盖项」（uncovered items）",
            "uncnone": "本运行配置下未检出重大缺口。",
            "item": "项目", "reason": "原因",
            "s17": "§22.17 分层验收声明（确定性层 vs LLM 依赖输出）",
            "s17note": "两层分开验收，严禁混报为单一「总体准确率」。",
            "det": "确定性工具层（可独立验收 · 可入 CM0）",
            "llm": "LLM 依赖输出层（禁入 CM4 · 复杂域须人工复核）",
            "comp": "组成", "metric": "指标", "accept": "验收",
            "ver": "技能版本（processDefinitionVersion，§22.5）",
            "preview": "（预览 — 运行 `--run` 后回填来源台账；coverage 暂显 n/a）",
        },
        "en": {
            "title": "AI-Generated-Asset Governance (ct-base §22)",
            "intro": "This skill is bound by ct-base §22. Literature retrieval / synthesis outputs are "
                     "RAG-style: conclusions are NEVER delivered without source traceability; uncovered "
                     "items are listed explicitly, never assumed complete (§22.16 + §17.1).",
            "s16": "§22.16 RAG three-column review checklist (Question / Source location / Basis)",
            "s16note": "Default failure mode = silent omission. Every point is traceable to its source "
                       "location and basis; a professional verifies against the original, AI does not "
                       "make the final call.",
            "q": "Question", "loc": "Source location", "basis": "Basis", "cov": "Covered",
            "yes": "✅ covered", "no": "⚠️ NOT covered",
            "unc": "§22.16 Explicit uncovered items",
            "uncnone": "No material gap detected for this run configuration.",
            "item": "Item", "reason": "Reason",
            "s17": "§22.17 Stratified acceptance (deterministic layer vs LLM-dependent output)",
            "s17note": "The two layers are verified SEPARATELY; never merged into one 'overall accuracy'.",
            "det": "Deterministic tool layer (independently verifiable · CM0-eligible)",
            "llm": "LLM-dependent output layer (CM4-forbidden · complex domains need human review)",
            "comp": "Components", "metric": "Metrics", "accept": "Acceptance",
            "ver": "Skill version (processDefinitionVersion, §22.5)",
            "preview": "(preview — run `--run` to populate the source ledger; coverage shown as n/a)",
        },
    }["zh" if zh else "en"]
    chk_rows = "".join(
        "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            esc(r["q"]), esc(r["location"]), esc(r["basis"]),
            esc(T["yes"] if r["covered"] else (T["no"] + ((" — " + r["note"]) if r["note"] else ""))))
        for r in g["checklist"])
    if g["uncovered"]:
        unc_rows = "".join(
            "<tr><td>{}</td><td>{}</td></tr>".format(esc(u["item"]), esc(u["reason"])) for u in g["uncovered"])
    else:
        unc_rows = '<tr><td colspan="2" class="empty">{}</td></tr>'.format(esc(T["uncnone"]))
    layers = ""
    for layer_key, heading in (("deterministic", T["det"]), ("llm", T["llm"])):
        blk = g["layers"][layer_key]
        layers += "<p><b>{}</b></p>".format(esc(heading))
        layers += "<ul><li><b>{}:</b> {}</li>".format(esc(T["comp"]), esc("; ".join(blk["components"])))
        layers += "<li><b>{}:</b> {}</li>".format(esc(T["metric"]), esc(blk["metrics"]))
        layers += "<li><b>{}:</b> {}</li></ul>".format(esc(T["accept"]), esc(blk["accept"]))
    return (
        '<h2>{}</h2>'.format(esc(T["title"]))
        + '<div class="prisma">'
        + '<p>{}</p>'.format(esc(T["intro"]))
        + '<h2 style="font-size:15px;margin-top:16px">{}</h2>'.format(esc(T["s16"]))
        + '<table><thead><tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr></thead><tbody>{}</tbody></table>'.format(
            esc(T["q"]), esc(T["loc"]), esc(T["basis"]), esc(T["cov"]), chk_rows)
        + '<p class="prisma-note">{}</p>'.format(esc(T["s16note"]))
        + '<h2 style="font-size:15px;margin-top:16px">{}</h2>'.format(esc(T["unc"]))
        + '<table><thead><tr><th>{}</th><th>{}</th></tr></thead><tbody>{}</tbody></table>'.format(
            esc(T["item"]), esc(T["reason"]), unc_rows)
        + '<h2 style="font-size:15px;margin-top:16px">{}</h2>'.format(esc(T["s17"]))
        + '<p class="prisma-note">{}</p>'.format(esc(T["s17note"]))
        + layers
        + '<p><b>{}:</b> {}{}</p>'.format(esc(T["ver"]), esc(g["version"]), esc(T["preview"] if not g["has_run"] else ""))
        + '</div>')

def render(data, lang, safety=False, report_first=False):
    # Resolve "auto" to a concrete language — never index _LABELS with the
    # literal "auto" (KeyError), and never inherit the server OS locale (the
    # published workbench runs in an en_US container -> was all-English).
    if lang == "auto":
        lang = resolve_report_lang(lang, skill="literature")
    L = _LABELS[lang]
    P = PALETTE
    # Coerce mixed / missing field types once (year as str, sources None, ...)
    # so sorting and joining below cannot abort the whole export.
    data = _sanitize(data)
    works = data.get("works") or []
    total = data.get("count") or len(works)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # search provenance (topic / generated keywords / filter) surfaced in the banner —
    # the user's original query and the skill's derived keywords must be reproducible
    # from the report itself, not just the evidence log.
    meta = data.get("meta") or {}
    _topic = meta.get("topic") or ""
    _topic_en = meta.get("topic_en") or ""
    if _topic_en and _topic_en != _topic:
        _topic_disp = "%s → %s" % (_topic, _topic_en)  # 中文检索词 → 翻译英文
    else:
        _topic_disp = _topic
    _kw = meta.get("keywords")
    if isinstance(_kw, str):
        _kw_str = _kw  # 兼容字符串直传（standalone 调用方）
    elif _kw:
        _kw_str = ", ".join(str(x) for x in _kw)
    else:
        _kw_str = ""
    _filters = []
    if meta.get("review_type") and meta.get("review_type") != "all":
        _filters.append("type=" + str(meta["review_type"]))
    if meta.get("year_from") or meta.get("year_to"):
        _filters.append("%s–%s" % (meta.get("year_from") or "?", meta.get("year_to") or "?"))
    _filter_str = " · ".join(_filters) if _filters else ""
    search_chips = []
    if _topic:
        search_chips.append(f'<span class="chip">{esc(L["search.topic"])}: <b>{esc(_topic_disp)}</b></span>')
    if _kw_str:
        search_chips.append(f'<span class="chip">{esc(L["search.keywords"])}: <b>{esc(_kw_str)}</b></span>')
    if _filter_str:
        search_chips.append(f'<span class="chip">{esc(L["search.filter"])}: <b>{esc(_filter_str)}</b></span>')
    # living-review delta (only when this run was merged against a previous one)
    _mg = meta.get("merge_existing")
    if isinstance(_mg, dict):
        search_chips.append(
            f'<span class="chip">{esc(L["merge.title"])}: '
            f'<b>{esc(L["merge.new"])}={_mg.get("new", 0)} · '
            f'{esc(L["merge.carry"])}={_mg.get("carryover", 0)} · '
            f'{esc(L["merge.retained"])}={_mg.get("retained_only", 0)}</b>'
            f' (@{esc(_mg.get("stamp", ""))})</span>')
    searchinfo = ('<div class="searchinfo">' + "".join(search_chips) + "</div>") if search_chips else ""

    years = sorted({w.get("year") for w in works if w.get("year")})
    year_span = f"{years[0]}–{years[-1]}" if years else "—"
    top_cited = max((w.get("cited_by_count") or 0) for w in works) if works else 0
    n_safety = sum(1 for w in works if w.get("is_safety"))
    n_pdf = sum(1 for w in works if w.get("local_pdf_path") and os.path.exists(w.get("local_pdf_path", "")))
    n_oa = sum(1 for w in works if w.get("open_access_url"))

    # KPI (safety KPI card only under --safety; the works-table amber highlight stays always-on)
    kpis = [(L["kpi.total"], str(total), "")]
    if safety:
        kpis.append((L["kpi.safety"], str(n_safety), ""))
    kpis += [
        (L["kpi.year"], esc(year_span), ""),
        (L["kpi.topcited"], str(top_cited), ""),
    ]
    kpi_html = "".join(
        f'<div class="kpi"><div class="kpi-label">{esc(lbl)}</div>'
        f'<div class="kpi-val">{esc(val)}</div><div class="kpi-sub">{esc(sub)}</div></div>'
        for lbl, val, sub in kpis
    )
    # U7: report-first progress indicator — shows which sections are filled vs pending
    rf_progress = ""
    if report_first:
        _rf_sections = [
            ("overview", True),           # always present
            ("works", bool(works)),
            ("prisma", bool(data.get("prisma"))),
            ("net", bool(works)),         # needs >= 2 docs with terms
            ("evidence", bool(data.get("evidence_log") or data.get("verification"))),
        ]
        _rf_filled = sum(1 for _, ok in _rf_sections if ok)
        _rf_steps = "".join(
            f'<span class="rf-step {"done" if ok else "pending"}">{"✓" if ok else "○"} {name}</span>'
            for name, ok in _rf_sections
        )
        rf_progress = (f'<div class="rf-progress">'
                       f'<div class="rf-bar"><div class="rf-fill" style="width:{_rf_filled * 100 // len(_rf_sections)}%"></div></div>'
                       f'<div class="rf-steps">{_rf_steps}</div>'
                       f'</div>')
    # "next steps" guidance strip shown to the end user on the report itself
    tips_html = (f'<div class="tips"><div class="tips-title">{esc(L["tips.title"])}</div><ol>'
                 f'<li>{esc(L["tips.t1"])}</li>'
                 f'<li>{esc(L["tips.t2"])}</li>'
                 f'<li>{esc(L["tips.t3"])}</li>'
                 f'<li>{esc(L["tips.t4"])}</li></ol></div>')
    # PDF 下载摘要
    pdf_summary = f'<div class="pdf-summary" style="margin-top:12px;padding:10px 14px;background:#e8f8f0;border-radius:8px;font-size:13px;">✓ PDF 已下载: <b>{n_pdf}</b> / {total} ｜ OA 链接: <b>{n_oa}</b> / {total}</div>' if n_pdf > 0 else ""

    # distributions
    src_c = Counter(w.get("source") for w in works)
    type_c = Counter(w.get("type") for w in works)
    year_c = Counter(w.get("year") for w in works)
    max_src = max(src_c.values()) if src_c else 1
    max_type = max(type_c.values()) if type_c else 1
    max_year = max(year_c.values()) if year_c else 1

    def dist_rows(counter, maxv):
        return "".join(
            f'<tr><td>{esc(k)}</td><td>{bar(v, maxv, P["blue"])}</td>'
            f'<td class="num">{v}</td></tr>'
            for k, v in counter.most_common()
        )
    src_rows = dist_rows(src_c, max_src)
    type_rows = dist_rows(type_c, max_type)
    year_rows = dist_rows(year_c, max_year)

    # works table
    wrows = ""
    for w in works:
        safe = w.get("is_safety")
        tr_cls = ' class="safety"' if safe else ""
        url = _html_link(w.get("url"))
        # preprint badge (R4: explicit "not peer-reviewed" labelling)
        is_pp = bool(w.get("preprint")) or (w.get("source") in ("bioRxiv", "medRxiv", "arXiv"))
        pp_badge = '<span class="pp">⚠️ 预印本</span> ' if is_pp else ""
        # source and id merged into one cell as two stacked lines
        # (database name on top, record id below); title itself links to the record
        src_full = w.get("source") or "—"
        rid = _short_id(w.get("id"))
        srcid_full = src_full + " · " + (w.get("id") or "—")
        srcid_html = (f'<span class="src">{esc(src_full)}</span>'
                      f'<span class="rid">{esc(rid)}</span>')
        title_html = (f'<a href="{esc(url)}" target="_blank" rel="noopener" title="{esc(w.get("title"))}">'
                      f'{esc(w.get("title"))}</a>' if url else esc(w.get("title") or "—"))
        oa_url = _html_link(w.get("open_access_url"))
        oa_link = f'<a href="{esc(oa_url)}" target="_blank" rel="noopener">OA</a>' if oa_url else "—"
        # abstract: full snippet with section labels re-flowed to paragraphs
        # (esc first, then newlines -> <br> so paragraph breaks survive HTML)
        abs_txt = restore_abstract_paragraphs((w.get("abstract_snippet") or "").strip())
        expandable = len(abs_txt) > 140
        abs_html = esc(abs_txt or "—").replace("\n\n", "<br><br>").replace("\n", "<br>")
        if expandable:
            abs_cell = (f'<span class="clip">{abs_html}</span>'
                        f'<span class="act" data-more="{esc(L["abs.more"])}" '
                        f'data-less="{esc(L["abs.less"])}">{esc(L["abs.more"])}</span>')
        else:
            abs_cell = abs_html
        auth_full = _fmt_authors(w.get("authors"), max_n=None)
        auth_show = _fmt_authors(w.get("authors"), max_n=4)
        _rs = w.get("relevance_score")
        _rel_cell = ("%.2f" % float(_rs)) if isinstance(_rs, (int, float)) else "—"
        _rel_title = esc(str(w.get("relevance_basis") or ""))
        wrows += (f'<tr{tr_cls}><td class="srcid" title="{esc(srcid_full)}">{srcid_html}</td>'
                  f'<td class="title">{pp_badge}{title_html}</td>'
                  f'<td class="abs{" expandable" if expandable else ""}">{abs_cell}</td>'
                  f'<td class="auths" title="{esc(auth_full)}">{esc(auth_show)}</td>'
                  f'<td class="num">{esc(w.get("year"))}</td><td>{esc(w.get("publication"))}</td>'
                  f'<td>{esc(w.get("type"))}</td><td>{esc(w.get("study_type"))}</td>'
                  f'<td class="num">{esc(w.get("cited_by_count"))}</td>'
                  f'<td class="num" title="{_rel_title}">{esc(_rel_cell)}</td>'
                  f'<td>{oa_link}</td></tr>')

    # safety subset — gated by --safety (mirrors the XLSX Safety-Related sheet):
    # a plain search must NOT emit the standalone subset; the is_safety amber
    # row-highlight inside the works table above remains always-on for scanning.
    safety_block = ""
    if safety:
        srows = ""
        for w in works:
            if not w.get("is_safety"):
                continue
            url = _html_link(w.get("url"))
            link = f'<a href="{esc(url)}" target="_blank" rel="noopener">↗</a>' if url else "—"
            abs_snip = restore_abstract_paragraphs((w.get("abstract_snippet") or "")[:220])
            abs_html = esc(abs_snip).replace("\n\n", "<br><br>").replace("\n", "<br>")
            srows += (f'<tr><td>{esc(w.get("source"))}</td><td>{esc(w.get("title"))}</td>'
                      f'<td class="num">{esc(w.get("year"))}</td><td>{esc(w.get("publication"))}</td>'
                      f'<td>{abs_html}{"…" if len(w.get("abstract_snippet") or "") > 220 else ""}</td>'
                      f'<td>{link}</td></tr>')
        if not srows:
            srows = f'<tr><td colspan="6" class="empty">—</td></tr>'
        safety_block = (f'<h2>{esc(L["safety"])}</h2>'
                        '<table><thead><tr><th>'
                        f'{esc(L["col.source"])}</th><th>{esc(L["col.title"])}</th>'
                        f'<th class="num">{esc(L["col.year"])}</th><th>{esc(L["col.pub"])}</th>'
                        f'<th>{esc(L["col.abstract"])}</th><th>{esc(L["col.link"])}</th>'
                        '</tr></thead><tbody>' + srows + '</tbody></table>')

    # PRISMA funnel (P0-B) — machine rule-based screen summary
    prisma = data.get("prisma")
    prisma_html = ""
    if prisma and prisma.get("stages"):
        svg = prisma_funnel_svg(prisma, P)
        rows = "".join(
            f'<tr><td>{esc(s.get("label", s.get("stage")))}</td>'
            f'<td class="num">{s.get("count")}</td></tr>'
            for s in prisma["stages"])
        reasons = prisma["stages"][2].get("reasons") if len(prisma["stages"]) > 2 else {}
        reason_txt = (" · ".join("%s=%d" % (k, v) for k, v in reasons.items())) if reasons else ""
        prisma_html = (
            f'<h2>PRISMA 筛选漏斗 / Screening funnel</h2>'
            f'<div class="prisma">{svg}'
            f'<table><thead><tr><th>Stage / 阶段</th><th class="num">n</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>'
            + (f'<div class="prisma-note">排除原因 / Excluded: {esc(reason_txt)}</div>' if reason_txt else "")
            + f'<div class="prisma-note">⚠️ {esc(prisma.get("note", ""))}</div>'
            f'</div>')
    else:
        # 轻量相关性概览（D 项）：未启用 --prisma 时默认给出，基于检索式的相关性机器辅助排序。
        # 明确标注为排序/提示用途，不构成最终纳入/排除裁决（呼应接缝护栏）；绝不静默丢文献。
        _rel = [float(w.get("relevance_score") or 0) for w in works]
        _n = len(_rel)
        _hi = sum(1 for r in _rel if r >= 0.5)
        _mid = sum(1 for r in _rel if 0.2 <= r < 0.5)
        _lo = sum(1 for r in _rel if r < 0.2)
        _pct = lambda x: ("%.0f%%" % (100.0 * x / _n)) if _n else "—"
        prisma_html = (
            f'<h2>{esc(L["rel.overview"])}</h2>'
            f'<div class="prisma-note">{esc(L["rel.overview.note"])}</div>'
            f'<table><thead><tr><th>{esc(L["rel.band"])}</th><th class="num">n</th>'
            f'<th class="num">{esc(L["rel.share"])}</th></tr></thead><tbody>'
            f'<tr><td>{esc(L["rel.high"])}</td><td class="num">{_hi}</td><td class="num">{_pct(_hi)}</td></tr>'
            f'<tr><td>{esc(L["rel.mid"])}</td><td class="num">{_mid}</td><td class="num">{_pct(_mid)}</td></tr>'
            f'<tr><td>{esc(L["rel.low"])}</td><td class="num">{_lo}</td><td class="num">{_pct(_lo)}</td></tr>'
            f'</tbody></table>')

    # Concept co-occurrence network (D) — inline SVG, stdlib-only, deterministic
    net_html = ""
    if works:
        net_svg = concept_network_svg(works, P)
        if net_svg:
            net_html = (f'<h2>{esc(L["net.title"])}</h2>'
                        f'<div class="prisma">{net_svg}'
                        f'<div class="prisma-note">{esc(L["net.note"])}</div></div>')

    # Evidence & verification (P0: provenance + citation verification, ct-base §17.1)
    evidence = data.get("evidence_log") or {}
    verification = data.get("verification") or {}
    evidence_html = ""
    if evidence or verification:
        blocks = []
        if verification:
            skip = (" · " + esc(L["ev.preview"])) if verification.get("skipped_preview") else ""
            vsum = (f'<div class="ev-verify"><b>{esc(L["ev.verify"])}:</b> '
                    f'{esc(L["ev.verified"])}={verification.get("verified", 0)} · '
                    f'{esc(L["ev.bot_blocked"])}={verification.get("bot_blocked", 0)} · '
                    f'{esc(L["ev.mismatch"])}={verification.get("mismatch", 0)} · '
                    f'{esc(L["ev.unresolved"])}={verification.get("unresolved", 0)} · '
                    f'{esc(L["ev.no_id"])}={verification.get("no_identifier", 0)} · '
                    f'{esc(L["ev.suspicious"])}={verification.get("suspicious", 0)}'
                    f'{esc(skip)}</div>')
            if verification.get("bot_blocked"):
                vsum += (f'<div class="ev-verify-note">{esc(L["ev.bot_blocked"])}'
                         f'={verification.get("bot_blocked", 0)}: '
                         f'{esc(L["ev.bot_blocked.note"])}</div>')
            if verification.get("mismatch"):
                vsum += (f'<div class="ev-verify-note">{esc(L["ev.mismatch"])}'
                         f'={verification.get("mismatch", 0)}: '
                         f'{esc(L["ev.mismatch.note"])}</div>')
            blocks.append(vsum)
        # run-time config audit: warn (with signup link) when the OpenAlex key is absent.
        # The HTML report is the primary deliverable since v0.6.8 (lit_report.md dropped),
        # so the key notice must live here too — otherwise it only exists in console output.
        _cfg = (evidence.get("config") or {}) if isinstance(evidence, dict) else {}
        if _cfg.get("openalex_key") == "missing":
            _u = esc(_cfg.get("openalex_key_url") or
                     "https://docs.openalex.org/about-openalex/api-key")
            blocks.append(
                f'<div class="ev-verify-note">⚠️ {esc(L["cfg.warn"])} '
                f'<a href="{_u}" target="_blank" rel="noopener">{_u}</a></div>')
        srcs = (evidence.get("sources") or []) if isinstance(evidence, dict) else []
        if srcs:
            rows = "".join(
                f'<tr><td>{esc(s.get("source"))}</td><td>{esc((s.get("query") or "")[:120])}</td>'
                f'<td>{esc(s.get("review_type") or "all")}</td>'
                f'<td>{esc(("%s–%s" % (s.get("year_from") or "", s.get("year_to") or "")) if (s.get("year_from") or s.get("year_to")) else "—")}</td>'
                f'<td>{esc("Y" if s.get("safety") else "—")}</td>'
                f'<td class="num">{esc(s.get("count", 0))}</td>'
                f'<td>{esc((s.get("retrieved_at") or "")[:19])}</td>'
                f'<td>{esc(s.get("status", ""))}</td></tr>'
                for s in srcs)
            blocks.append(
                f'<table><thead><tr><th>{esc(L["ev.src"])}</th><th>{esc(L["ev.query"])}</th>'
                f'<th>{esc(L["ev.type"])}</th><th>{esc(L["ev.year"])}</th>'
                f'<th>{esc(L["ev.safety"])}</th><th class="num">{esc(L["ev.count"])}</th>'
                f'<th>{esc(L["ev.retrieved"])}</th><th>{esc(L["ev.status"])}</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
        if not blocks:
            blocks.append('<div class="ev-verify">—</div>')
        # R6: source-status summary (tool-error != empty-result)
        if srcs:
            _st = {}
            for s in srcs:
                _st[s.get("status", "ok")] = _st.get(s.get("status", "ok"), 0) + 1
            blocks.append(
                f'<div class="ev-verify-note">{esc(L["ev.src_summary"])}: '
                f'{_st.get("ok", 0)} OK · {_st.get("error", 0)} error · '
                f'{_st.get("skipped", 0)} skipped · {_st.get("empty", 0)} empty</div>')
        ev_note = ('<div class="prisma-note">Provenance audit trail (ct-base §17.1): '
                   'every evidence item is traceable to its source query and retrieval time. '
                   'Verification status is advisory, not a substitute for human review. / '
                   '证据溯源审计（ct-base §17.1）：每条证据可回溯至来源检索式与检索时间；'
                   '验证状态仅供参考，不替代人工核查。</div>')
        # R3: citation count ≠ quality disclaimer
        ev_note += f'<div class="prisma-note">{esc(L["cite.foot"])}</div>'
        evidence_html = (
            f'<h2>{esc(L["evidence"])}</h2>'
            f'<div class="prisma">{"".join(blocks)}{ev_note}</div>')

    # ---- ct-base §22 governance (§22.16 RAG checklist + §22.17 stratified acceptance) ----
    gov22_html = _gov22_html(data, lang)

    css = f"""
    :root {{ --navy:{P['navy']}; --blue:{P['blue']}; --light:{P['light']};
            --banner:{P['banner']}; --grid:{P['grid']}; --greytx:{P['greytx']};
            --warn:{P['warn_bg']}; --warnbd:{P['warn_bd']}; }}
    * {{ box-sizing:border-box; }}
    body {{ font-family:'Microsoft YaHei','PingFang SC',sans-serif; margin:0;
            color:#1a1a1a; background:#f5f7f8; }}
    .banner {{ background:linear-gradient(135deg,var(--navy),var(--banner)); color:#fff;
               padding:22px 28px; }}
    .banner h1 {{ margin:0; font-size:22px; }}
    .banner .meta {{ margin-top:6px; font-size:12px; opacity:.85; }}
    .banner .searchinfo {{ margin-top:8px; font-size:12px; display:flex; flex-wrap:wrap; gap:6px; }}
    .banner .searchinfo .chip {{ background:rgba(255,255,255,.15); border-radius:10px;
      padding:2px 10px; opacity:.95; }}
    .banner .searchinfo .chip b {{ font-weight:600; }}
    .banner .pp {{ background:#fff5d6; color:#8a5a00; border-radius:12px;
      padding:2px 10px; font-size:11px; font-weight:600; }}
    .wrap {{ max-width:1180px; margin:0 auto; padding:20px 24px 60px; }}
    h2 {{ color:var(--navy); border-left:5px solid var(--blue); padding-left:10px;
          margin-top:30px; font-size:17px; }}
    .kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:18px; }}
    .kpi {{ background:#fff; border:1px solid var(--grid); border-radius:10px; padding:16px;
            box-shadow:0 1px 3px rgba(0,0,0,.06); }}
    .kpi-label {{ font-size:12px; color:var(--greytx); }}
    .kpi-val {{ font-size:24px; font-weight:700; color:var(--navy); margin-top:4px; }}
    .pdf-summary {{ margin-top:12px; padding:10px 14px; background:#e8f8f0; border-radius:8px; font-size:13px; }}
    .pdf-summary b {{ color:var(--navy); }}
    .tips {{ margin-top:14px; background:var(--light); border:1px solid var(--grid); border-radius:8px;
             padding:10px 16px 8px; font-size:12.5px; color:#333; }}
    .tips .tips-title {{ font-weight:700; color:var(--navy); margin-bottom:4px; }}
    .tips ol {{ margin:0; padding-left:18px; }}
    .tips li {{ margin:2px 0; line-height:1.5; }}
    table {{ width:100%; border-collapse:collapse; background:#fff; margin-top:12px;
             border:1px solid var(--grid); border-radius:8px; overflow:hidden; }}
    th,td {{ padding:9px 11px; text-align:left; border-bottom:1px solid var(--grid);
             font-size:13px; vertical-align:top; }}
    th {{ background:var(--light); color:var(--navy); font-weight:600; position:sticky; top:0; }}
    tr:nth-child(even) td {{ background:#fafcfb; }}
    tr.safety td {{ background:var(--warn); }}
    tr.safety td:first-child {{ border-left:4px solid var(--warnbd); }}
    /* works table: source·id wraps (short ids, ≤2 lines); title gets an
       explicit generous share; authors collapse to one ellipsized line so
       they never squeeze the title; compact padding keeps records short */
    table.works th, table.works td {{ padding:5px 8px; }}
    table.works td.srcid {{ max-width:150px; }}
    table.works td.srcid .src {{ display:block; font-size:12px; color:#556; }}
    table.works td.srcid .rid {{ display:block; font-size:12px; color:#667; word-break:break-all; }}
    table.works td.title {{ width:24%; min-width:240px; word-break:break-word; }}
    table.works td.auths {{ max-width:180px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
    table.works td.title a {{ color:var(--navy); font-weight:600; text-decoration:none; }}
    table.works td.title a:hover {{ color:var(--blue); text-decoration:underline; }}
    table.works th.abs, table.works td.abs {{ width:30%; min-width:280px; word-break:break-word; }}
    /* abstract: collapsed to 2 lines by default; click the cell to expand */
    table.works td.abs.expandable {{ cursor:pointer; }}
    table.works td.abs .clip {{ display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }}
    table.works td.abs.open .clip {{ display:block; -webkit-line-clamp:unset; }}
    table.works td.abs .act {{ color:var(--blue); font-size:11px; user-select:none; margin-left:2px; white-space:nowrap; }}
    .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
    .empty {{ color:var(--greytx); text-align:center; }}
    .barwrap {{ position:relative; min-width:150px; }}
    .bar {{ height:14px; border-radius:4px; display:inline-block; vertical-align:middle; }}
    .barval {{ margin-left:8px; font-size:12px; color:var(--greytx); }}
    .dist {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px; }}
    .prisma {{ background:#fff; border:1px solid var(--grid); border-radius:10px;
               padding:16px; margin-top:14px; }}
    .prisma svg {{ display:block; max-width:620px; margin:0 auto 10px; }}
    .prisma table {{ max-width:420px; margin:0 auto; }}
    .prisma-note {{ font-size:12px; color:var(--greytx); margin-top:8px; text-align:center; }}
    /* U7: report-first progress bar */
    .rf-progress {{ margin-top:14px; background:#fff; border:1px solid var(--grid); border-radius:8px; padding:12px 16px; }}
    .rf-bar {{ height:8px; background:#e8ecef; border-radius:4px; overflow:hidden; }}
    .rf-fill {{ height:100%; background:var(--blue); border-radius:4px; transition:width .3s ease; }}
    .rf-steps {{ display:flex; gap:12px; margin-top:8px; flex-wrap:wrap; font-size:12px; }}
    .rf-step {{ padding:2px 8px; border-radius:10px; }}
    .rf-step.done {{ background:#e8f8f0; color:#1a6b3a; }}
    .rf-step.pending {{ background:#f0f0f0; color:#999; }}
    @media (max-width:880px) {{ .dist {{ grid-template-columns:1fr; }} .kpis {{ grid-template-columns:repeat(2,1fr); }} }}
    @media print {{
      @page {{ margin:12mm; }}
      * {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
      body {{ background:#fff; color:#000; }}
      .banner {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; color:#fff; }}
      .wrap {{ max-width:none; padding:0; }}
      .kpi, table, ul, h2, .dist {{ break-inside:avoid; }}
      a {{ color:#000; text-decoration:none; }}
      .bar {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
      tr.safety td {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
    }}
    """

    return f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(L['doc_title'])}</title>
<style>{css}</style></head>
<body>
<div class="banner"><h1>{esc(L['doc_title'])}</h1>
<div class="meta">{esc(L['generated'])}: {now} ｜ {total} works</div>
<div class="meta">{esc(L['src.banner'])}</div>{searchinfo}</div>
<div class="wrap">
  <div class="kpis">{kpi_html}</div>
  {rf_progress}
  {pdf_summary}
  {tips_html}

  <h2>{esc(L['overview'])}</h2>
  <div class="dist">
    <div><table><thead><tr><th>{esc(L['by_src'])}</th><th></th><th class="num">n</th></tr></thead><tbody>{src_rows}</tbody></table></div>
    <div><table><thead><tr><th>{esc(L['by_type'])}</th><th></th><th class="num">n</th></tr></thead><tbody>{type_rows}</tbody></table></div>
    <div><table><thead><tr><th>{esc(L['by_year'])}</th><th></th><th class="num">n</th></tr></thead><tbody>{year_rows}</tbody></table></div>
  </div>

  <h2>{esc(L['works'])}</h2>
  <table class="works"><thead><tr><th>{esc(L['col.srcid'])}</th><th>{esc(L['col.title'])}</th>
  <th class="abs">{esc(L['col.abstract'])}</th>
  <th>{esc(L['col.authors'])}</th><th class="num">{esc(L['col.year'])}</th><th>{esc(L['col.pub'])}</th>
  <th>{esc(L['col.type'])}</th><th>{esc(L['col.study'])}</th><th class="num">{esc(L['col.cited'])}</th>
  <th class="num">{esc(L['col.relevance'])}</th>
  <th>{esc(L['col.oa'])}</th>
  </tr></thead>
  <tbody>{wrows}</tbody></table>

  {safety_block}

  {prisma_html}
  {net_html}
  {evidence_html}
  {gov22_html}
</div>
<script>
/* expand / collapse long abstracts in the works table (click the abstract cell) */
document.addEventListener('click', function(e) {{
  var t = e.target.closest('td.abs.expandable');
  if (!t) return;
  var open = t.classList.toggle('open');
  var a = t.querySelector('.act');
  if (a) a.textContent = open ? a.dataset.less : a.dataset.more;
}});
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-json", default=".merged.json",
                    help=".merged.json (hidden intermediate from ct_literature)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    ap.add_argument("--safety", action="store_true",
                    help="emit the standalone Safety / CSM subset section (off by default)")
    args = ap.parse_args()
    data = json.load(open(args.in_json, encoding="utf-8"))
    html_out = render(data, args.lang, safety=args.safety)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"HTML written: {args.out} ({len(html_out)} bytes, lang={args.lang})")


if __name__ == "__main__":
    main()
