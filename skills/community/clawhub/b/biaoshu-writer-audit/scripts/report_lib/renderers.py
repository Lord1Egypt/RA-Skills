"""Service-specific report renderers."""

from datetime import datetime

from .common import (
    _DUP_CAT_ZH,
    _DUP_FRAGMENT_LIMIT_PER_PAIR,
    _DUP_ROLE_ZH,
    _DUP_RISK_BUCKET,
    _DUP_RISK_LABEL,
    _DUP_RISK_LIMIT_PER_PAIR,
    _DUP_STRENGTH_ZH,
    _PRIORITY_ZH,
    _RISK_LABEL,
    _clean_text,
    _dup_evidence_note,
    _eval_rows,
    _ev,
    _filesize,
    _flatten_named,
    _g,
    _group_rows,
    _partial_summary_items,
    _project_name,
    _risk_bucket,
    _semantic_review_lines,
    _sim_score,
)
from .writers import Report


def _file_extra(item):
    fmt = _clean_text(_g(item, "format", default=""))
    size = _filesize(_g(item, "size_bytes"))
    return " · ".join(x for x in (fmt, size if size != "-" else "") if x)


# ============================== 解读报告 ==============================
def render_interpretation(result):
    r = Report("招标文件智能解读报告")
    pid = _g(result, "project_id", default="-")
    pinfo = _g(result, "project_info", default=[]) or []
    cover_title = _project_name(pinfo) or "招标文件智能解读报告"
    r.cover("Intelligent Interpretation · 智能解读", cover_title,
            [("项目句柄", f"project_id {pid}"), ("生成时间", f"{datetime.now():%Y-%m-%d %H:%M}")])

    n0 = len(r.blocks)
    if pinfo:
        r.h2("一、项目基本信息")
        r.facts([(_g(it, "field_name", default=""), _clean_text(_g(it, "field_value", default="")))
                 for it in pinfo if isinstance(it, dict)])

    da = _g(result, "decision_analysis", default={}) or {}
    if da:
        r.h2("二、控标洞察（竞争分析）")
        r.callout(f"投标建议：{_g(da,'participation_recommendation',default='-')}　|　"
                  f"控标风险：{_g(da,'control_risk_level',default='-')}　|　"
                  f"分析置信度：{_g(da,'confidence_level',default='-')}")
        for s in (_g(da, "summary", default=[]) or []):
            text = _clean_text(s)
            if text:
                r.bullet(text)
        for sig in (_g(da, "signals", default=[]) or []):
            rc = _risk_bucket(_g(sig, "risk_level"))
            badge = _RISK_LABEL.get(rc, str(_g(sig, "risk_level", default="-")))
            note = ("判定依据：" + _g(sig, "reasoning", default="")) if _g(sig, "reasoning") else ""
            r.signal_card(rc, badge, _g(sig, "title", default=""), _g(sig, "description", default=""), note)
        acts = _g(da, "actions", default=[]) or []
        if acts:
            r.h3("行动建议")
            for a in acts:
                prio = _PRIORITY_ZH.get(str(_g(a, "priority")), _g(a, "priority", default="-"))
                rec = _clean_text(_g(a, "recommendation", default=""))
                if rec:
                    r.prio_bullet(prio, rec)
        gap = _g(da, "our_gap_assessment", default=[]) or []
        if gap:
            r.h3("我方差距 / 优势")
            for g in gap:
                text = _clean_text(g)
                if text:
                    r.bullet(text)

    def list_section(title, key, head_keys, body_key):
        groups = _group_rows(_g(result, key, default=[]) or [], head_keys, body_key)
        if not groups:
            return
        r.h2(title)
        for head, items in groups:
            r.req_group(head, items)

    list_section("三、合标项要求（参与资格）", "compliance", ["category"], "requirement_text")
    list_section("四、废标项要求（红线）", "disqualification", ["type", "category"], "requirement_text")
    ev_rows = _eval_rows(_g(result, "evaluation", default=[]) or [])
    if ev_rows:
        r.h2("五、评审项（评分标准）")
        r.eval_table(ev_rows)
    list_section("六、关键要求", "key_requirements", ["category"], "requirement_text")
    list_section("七、商务条款", "business_terms", ["term_type"], "term_content")
    list_section("八、报价要求", "pricing", ["component"], "requirement_text")

    pa = _g(result, "procurement_analysis", default={}) or {}
    if pa:
        r.h2("九、采购背景与需求分析")
        bg = _clean_text(_g(pa, "procurement_background", default=""))
        obj = _clean_text(_g(pa, "procurement_objectives", default=""))
        scope = _flatten_named(_g(pa, "procurement_scope_items", default=[]) or [])
        constraints = _flatten_named(_g(pa, "key_constraints", default=[]) or [])
        metrics = _flatten_named(_g(pa, "key_success_metrics", default=[]) or [])
        structured = any([bg, obj, scope, constraints, metrics])
        summary = _clean_text(_g(pa, "analysis_summary", default=""))
        if summary and not structured:
            r.p(summary)
        if bg:
            r.h3("采购背景")
            r.p(bg)
        if obj:
            r.h3("采购目标")
            r.p(obj)
        if scope:
            r.h3("采购范围")
            r.named_cards(scope)
        if constraints:
            r.h3("关键约束")
            r.named_cards(constraints)
        if metrics:
            r.h3("关键成功指标")
            r.named_cards(metrics)

    if len(r.blocks) <= n0:
        r.p("⚠️ 本次解读结果未包含结构化内容字段（后端可能未按文档返回完整数据），无可渲染明细。")
    return r.render_html(), r.blocks

# ============================== 合规报告 ==============================
def render_compliance(result):
    comp = result.get("compliance") if isinstance(result, dict) and isinstance(
        result.get("compliance"), dict) else result
    r = Report("合规审查报告")

    summary = _g(comp, "summary", default={}) or {}
    bid_files = [f for f in (_g(comp, "bid_files", default=[]) or []) if isinstance(f, dict)]
    issues = [i for i in (_g(comp, "issues", default=[]) or []) if isinstance(i, dict)]
    sims = [s for s in (_g(comp, "similarity_issues", default=[]) or []) if isinstance(s, dict)]
    manual = [m for m in (_g(comp, "manual_items", default=[]) or []) if isinstance(m, dict)]
    scope = _g(comp, "scope_summary_lines", default=[]) or []
    partial = _g(comp, "partial_summary", default={}) or {}

    file_names = [str(_g(f, "filename", default="")).strip() for f in bid_files]
    cover_title = file_names[0] if len(file_names) == 1 else (
        f"{file_names[0]} 等 {len(file_names)} 份" if file_names else "合规审查报告")
    r.cover("Compliance Review · 合规审查", cover_title,
            [("审查对象", "、".join(file_names) if file_names else "-"),
             ("生成时间", f"{datetime.now():%Y-%m-%d %H:%M}")])

    def _i(k):
        try:
            return int(_g(summary, k, default=0) or 0)
        except (TypeError, ValueError):
            return 0

    r.h2("一、风险概览")
    r.risk_bar(_i("high_count"), _i("review_count"), _i("tip_count"))
    r.metrics([
        ("高风险", _i("high_count"), "high"),
        ("待复核", _i("review_count"), "review"),
        ("提示项", _i("tip_count"), "tip"),
        ("多文件雷同", _i("similarity_count"), "ok"),
        ("手动待确认", _i("manual_unchecked_count"), "ok"),
    ])
    if _g(summary, "conclusion"):
        r.callout(_clean_text(_g(summary, "conclusion", default="")))
    semantic_lines = _semantic_review_lines(summary)
    if semantic_lines:
        r.h3("审查完整性")
        for line in semantic_lines:
            r.bullet(line)
    partial_items = _partial_summary_items(partial)
    if partial_items:
        r.h3("阶段性/部分结果摘要")
        for line in partial_items:
            r.bullet(line)
    for line in scope:
        text = _clean_text(line)
        if text:
            r.bullet(text)
    if bid_files:
        r.h3("审查文件")
        r.file_rows([
            ("投标文件", _g(f, "filename", default="-"), _file_extra(f))
            for f in bid_files
        ])

    def block(it):
        rc = _risk_bucket(_g(it, "risk_level"))
        r.issue_card(rc, _RISK_LABEL.get(rc, str(_g(it, "risk_level", default="-"))),
                     _clean_text(_g(it, "title", default="")),
                     _clean_text(_g(it, "bid_filename", default="")),
                     _clean_text(_g(it, "description", default="")),
                     _ev(_g(it, "tender_evidence", "tender_evidence_json", default={})),
                     _ev(_g(it, "bid_evidence", "bid_evidence_json", default={})),
                     _clean_text(_g(it, "suggestion", default="")))

    highs = [i for i in issues if _risk_bucket(_g(i, "risk_level")) == "high"]
    reviews = [i for i in issues if _risk_bucket(_g(i, "risk_level")) == "review"]
    tips = [i for i in issues if _risk_bucket(_g(i, "risk_level")) == "tip"]

    r.h2("二、高风险问题（优先修改）")
    if highs:
        for it in highs:
            block(it)
    else:
        r.ok_line("未发现高风险问题。")

    if reviews:
        r.h2(f"三、待人工复核（{len(reviews)} 项）")
        for it in reviews:
            block(it)
    if tips:
        r.h2(f"四、提示项（格式 / 规范，{len(tips)} 项）")
        for it in tips:
            r.tip_row(_clean_text(_g(it, "title", default="")),
                      _clean_text(_g(it, "description", default="")))

    if sims:
        r.h2("五、多文件相似度（串标风险）")
        for s in sims:
            rc = _risk_bucket(_g(s, "risk_level"))
            pair = " ↔ ".join(x for x in (
                _clean_text(_g(s, "file_a_name", default="")),
                _clean_text(_g(s, "file_b_name", default="")),
            ) if x)
            score = _sim_score(_g(s, "similarity_score", default=""))
            title = _clean_text(_g(s, "title", default=""))
            note = "　".join(x for x in (pair, f"相似度 {score}" if score not in ("", "-") else "") if x)
            r.signal_card(rc, _RISK_LABEL.get(rc, str(_g(s, "risk_level", default="-"))),
                          title, _clean_text(_g(s, "suggestion", default="")), note)

    if manual:
        r.h2("六、手动核查清单")
        by_cat = {}
        for m in manual:
            by_cat.setdefault(_g(m, "category", default="其他") or "其他", []).append(m)
        for cat, items in by_cat.items():
            r.h3(cat)
            for m in items:
                desc = _clean_text(_g(m, "description", default=""))
                title = _clean_text(_g(m, "title", default=""))
                if desc == title:
                    desc = ""
                r.check_item(bool(_g(m, "is_checked")), title,
                             _clean_text(_g(m, "note", default="")), desc)

    if not issues and not sims and not manual and not summary:
        r.p("⚠️ 本次合规结果为空（后端可能未按文档返回完整数据）。")
    return r.render_html(), r.blocks

# ============================== 查重报告 ==============================
def render_bid_duplicate(result):
    dup = result.get("duplicate") if isinstance(result, dict) and isinstance(
        result.get("duplicate"), dict) else result
    dup = dup if isinstance(dup, dict) else {}
    r = Report("标书查重报告")

    summary = _g(dup, "summary", default={}) or {}
    if not summary and any(dup.get(k) for k in ("file_count", "pair_count", "risk_counts")):
        summary = dup
    files = [f for f in (_g(dup, "files", default=[]) or []) if isinstance(f, dict)]
    pairs = [p for p in (_g(dup, "pairs", default=[]) or []) if isinstance(p, dict)]
    risk_counts = summary.get("risk_counts") if isinstance(summary.get("risk_counts"), dict) else {}
    run_id = _g(dup, "run_id", default=_g(result, "run_id", default="-"))
    bid_names = [str(_g(item, "filename", default="")).strip()
                 for item in files if _g(item, "role") != "tender"]
    cover_title = " ↔ ".join(bid_names[:2]) if len(bid_names) >= 2 else (bid_names[0] if bid_names else "标书查重报告")
    r.cover("Bid Duplicate Review · 标书查重", cover_title,
            [("任务编号", f"run_id {run_id}"),
             ("投标文件", "、".join(bid_names) or "-"),
             ("生成时间", f"{datetime.now():%Y-%m-%d %H:%M}")])

    def _count(key):
        try:
            return int(risk_counts.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0

    high, medium, low = _count("high"), _count("medium"), _count("low")
    r.h2("一、风险概览")
    r.risk_bar(high, medium, low)
    r.metrics([
        ("投标文件数", _g(summary, "file_count", default=len([f for f in files if _g(f, "role") == "bid"])), "ok"),
        ("文件组合数", _g(summary, "pair_count", default=len(pairs)), "ok"),
        ("高风险组合", high, "high"),
        ("中风险组合", medium, "review"),
        ("低风险组合", low, "tip"),
    ])
    r.callout("本报告用于投标文件提交前内部自查，仅呈现雷同/相似风险线索，不构成围标、串标、违法违规或投标有效性的法律认定。")

    options = _g(dup, "options", default={}) or {}
    if options:
        r.h3("检查选项")
        r.facts([
            (label, "开启" if bool(options.get(key)) else "关闭")
            for label, key in (
                ("图片相似检查", "enable_image"),
                ("文档元数据检查", "enable_metadata"),
                ("语义相似检查", "enable_semantic"),
                ("排除招标原文共同表述", "exclude_tender_baseline"),
            ) if key in options
        ])

    if files:
        r.h2("二、参与文件")
        r.file_rows([
            ("招标文件" if _g(item, "role") == "tender" else "投标文件",
             _g(item, "filename", default="-"),
             _file_extra(item))
            for item in files
        ])

    warnings = summary.get("parse_warnings") if isinstance(summary, dict) else []
    warnings = [item for item in (warnings or []) if isinstance(item, dict)]
    if warnings:
        r.h2("三、解析告警")
        for item in warnings:
            r.bullet(" · ".join(x for x in (
                _clean_text(_g(item, "role", default="")),
                _clean_text(_g(item, "filename", default="")),
                _clean_text(_g(item, "code", default="")),
                _clean_text(_g(item, "message", default="")),
            ) if x))

    pair_section_title = "四、文件组合判定" if warnings else "三、文件组合判定"
    r.h2(pair_section_title)
    if not pairs:
        r.p("未生成文件组合。")
    for idx, pair in enumerate(pairs, 1):
        raw_level = str(_g(pair, "risk_level", default="other") or "other")
        rc = _DUP_RISK_BUCKET.get(raw_level, "other")
        badge = _DUP_RISK_LABEL.get(raw_level, _DUP_RISK_LABEL["other"])
        fa = _clean_text(_g(pair, "file_a_name", default="文件A"))
        fb = _clean_text(_g(pair, "file_b_name", default="文件B"))
        r.signal_card(rc, badge, f"{idx}. {fa} ↔ {fb}", "", "")
        r.meters([
            ("综合重复率", _g(pair, "combined_text_rate")),
            ("章节加权", _g(pair, "weighted_combined_text_rate")),
            ("文件A覆盖", _g(pair, "file_a_coverage_rate")),
            ("文件B覆盖", _g(pair, "file_b_coverage_rate")),
        ])
        reasons = _g(_g(pair, "summary", default={}) or {}, "reasons", default=[]) or []
        if reasons:
            r.h3("判级依据")
            for reason in reasons[:8]:
                text = _clean_text(reason)
                if text:
                    r.bullet(text)

        risks = [item for item in (_g(pair, "risks", default=[]) or []) if isinstance(item, dict)]
        if risks:
            shown = risks[:_DUP_RISK_LIMIT_PER_PAIR]
            r.h3(f"非文本风险线索（展示 {len(shown)} / {len(risks)} 条）")
            for risk in shown:
                cat = _DUP_CAT_ZH.get(str(_g(risk, "category", default="")), _g(risk, "category", default="线索"))
                strength = _DUP_STRENGTH_ZH.get(str(_g(risk, "strength", default="")), _g(risk, "strength", default=""))
                badge_r = f"{cat}" + (f" · {strength}" if strength else "")
                r.signal_card(rc, badge_r,
                              _clean_text(_g(risk, "explanation", default="")),
                              _dup_evidence_note(_g(risk, "evidence", default={})), "")

        fragments = [item for item in (_g(pair, "fragments", default=[]) or []) if isinstance(item, dict)]
        if fragments:
            shown_f = fragments[:_DUP_FRAGMENT_LIMIT_PER_PAIR]
            r.h3(f"文本重复证据（展示 {len(shown_f)} / {len(fragments)} 条）")
            for fragment in shown_f:
                role = _DUP_ROLE_ZH.get(str(_g(fragment, "section_role", default="")),
                                        _g(fragment, "section_role", default="") or "未分类")
                chars = _g(fragment, "normalized_chars", default="-")
                r.compare(f"{role} · {chars} 字",
                          _clean_text(_g(fragment, "text_a", default="")),
                          _clean_text(_g(fragment, "text_b", default="")),
                          fa, fb)

    if not summary and not files and not pairs:
        r.p("⚠️ 本次查重结果为空（后端可能未按文档返回完整数据）。")
    return r.render_html(), r.blocks


RENDERERS = {
    "interpretation": render_interpretation,
    "compliance": render_compliance,
    "bid_duplicate": render_bid_duplicate,
}
