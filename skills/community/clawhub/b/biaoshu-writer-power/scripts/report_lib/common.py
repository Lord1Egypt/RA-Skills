"""Common data helpers and constants for report rendering."""

import ast
import json
import os
import re

# ============================== 配色/常量 ==============================
# 风险分桶：兼容真实后端(high/review/tip) 与文档(高/中/低)
def _risk_bucket(level):
    s = str(level)
    if s in ("高", "high"):
        return "high"
    if s in ("中", "review"):
        return "review"
    if s in ("低", "tip"):
        return "tip"
    return "other"


_RISK_LABEL = {"high": "高风险", "review": "待复核", "tip": "提示", "other": "其他"}
# 行动建议优先级 high/medium/low → 中文
_PRIORITY_ZH = {"high": "高", "medium": "中", "low": "低"}
_SEMANTIC_STATE_ZH = {
    "full": "完整完成",
    "complete": "完整完成",
    "completed": "完整完成",
    "done": "完整完成",
    "rules_only": "仅规则检查",
    "semantic_partial": "部分完成",
    "partial": "部分完成",
    "running": "处理中",
    "processing": "处理中",
    "pending": "等待处理",
    "failed": "异常",
    "error": "异常",
    "skipped": "未执行",
}
_DOCX_RISK_COLOR = {"high": "C0392B", "review": "B9770E", "tip": "0E7490", "other": "475569"}
_LABEL = {"interpretation": "智能解读", "compliance": "合规审查", "bid_duplicate": "标书查重"}
_DUP_RISK_LABEL = {"high": "高风险", "medium": "中风险", "low": "低风险", "other": "其他"}
_DUP_RISK_BUCKET = {"high": "high", "medium": "review", "low": "tip"}
_DUP_FRAGMENT_LIMIT_PER_PAIR = 20
_DUP_RISK_LIMIT_PER_PAIR = 20


def _safe_name(name):
    name = os.path.splitext(os.path.basename(str(name)))[0]
    for ch in '/\\:*?"<>|':
        name = name.replace(ch, "_")
    return name.strip() or "report"

def _unwrap(data):
    if isinstance(data, dict) and "result" in data and "service" in data:
        return data.get("service"), (data.get("result") or {})
    if isinstance(data, dict) and ("duplicate" in data or "pairs" in data):
        return "bid_duplicate", data
    if isinstance(data, dict) and ("issues" in data or "run_id" in data or "compliance" in data):
        return "compliance", data
    return "interpretation", (data or {})


def _g(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d and d[k] is not None:
            return d[k]
    return default


_BLANK_TEXT = {
    "无", "无相关条款", "无相关描述", "无相关里程碑要求描述",
    "未在招标文件中明确提及", "（无相关条款）", "(无相关条款)",
}
_NAME_KEYS = ("name", "title", "field_name", "名称")
_DETAIL_KEYS = ("detail", "description", "field_value", "requirement_text",
                "term_content", "text", "content", "说明", "内容")
_SKIP_STRUCT_KEYS = {
    "id", "source_page", "source_text", "is_structured", "source_anchor", "weight",
}


def _clean_text(text):
    """Collapse PDF extraction whitespace and stray separators into readable prose."""
    if text is None:
        return ""
    s = str(text).replace("\u3000", " ").replace("||||", " ")
    s = re.sub(r"[|｜]{2,}", " ", s)
    lines = [" ".join(ln.split()) for ln in s.splitlines()]
    return " ".join(ln for ln in lines if ln).strip()


def _is_blank(text):
    s = _clean_text(text)
    if not s:
        return True
    compact = s.replace("（", "").replace("）", "").replace("(", "").replace(")", "").strip()
    return s in _BLANK_TEXT or compact in _BLANK_TEXT


def _as_struct(value):
    """Turn a dict/list, or a JSON / Python-literal string of one, into a structure."""
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return value
    s = value.strip()
    if len(s) < 2 or s[0] not in "{[" or s[-1] not in "}]":
        return value
    for loader in (json.loads, ast.literal_eval):
        try:
            parsed = loader(s)
        except (ValueError, SyntaxError, json.JSONDecodeError, TypeError):
            continue
        if isinstance(parsed, (dict, list)):
            return parsed
    return value


def _dedupe_labels(vals):
    out = []
    for raw in vals:
        v = _clean_text(raw)
        if not v:
            continue
        if any(v == x or v in x for x in out):
            continue
        out = [x for x in out if x not in v]
        out.append(v)
    return out


def _named_parts(value):
    """Normalize a constraint/scope item to (name, detail, page) or None if empty."""
    value = _as_struct(value)
    if isinstance(value, list):
        return [_named_parts(x) for x in value]
    page = ""
    if isinstance(value, dict):
        page = value.get("source_page") or ""
        name = next((str(value[k]).strip() for k in _NAME_KEYS if value.get(k)), "")
        detail = ""
        for k in _DETAIL_KEYS:
            if value.get(k) not in (None, ""):
                detail = str(value[k]).strip()
                break
        if not name and not detail:
            bits = []
            for k, v in value.items():
                if k in _SKIP_STRUCT_KEYS or v in (None, "", [], {}):
                    continue
                if isinstance(v, (dict, list)):
                    continue
                bits.append(f"{k}：{v}")
            detail = "；".join(bits)
        name, detail = _clean_text(name), _clean_text(detail)
        if _is_blank(name) and _is_blank(detail):
            return None
        return (name, detail, page)
    text = _clean_text(value)
    if _is_blank(text):
        return None
    return ("", text, page)


def _flatten_named(items):
    out = []
    for item in items or []:
        parsed = _named_parts(item)
        if parsed is None:
            continue
        if isinstance(parsed, list):
            out.extend(x for x in parsed if x)
        else:
            out.append(parsed)
    return out


def _group_rows(rows, head_keys, body_key):
    """Group requirement rows by category, dropping blank / placeholder bodies."""
    groups = []
    index = {}
    for it in rows or []:
        if not isinstance(it, dict):
            parsed = _named_parts(it)
            if not parsed or isinstance(parsed, list):
                continue
            name, detail, page = parsed
            body = detail or name
            if _is_blank(body):
                continue
            head = name or "其他"
            rec = {"body": body, "page": page, "source": ""}
        else:
            body = _clean_text(_g(it, body_key, default=""))
            if _is_blank(body):
                continue
            head = " · ".join(_dedupe_labels(_g(it, f, default="") for f in head_keys)) or "其他"
            source = _clean_text(_g(it, "source_text", default=""))
            if source == body:
                source = ""
            rec = {"body": body, "page": _g(it, "source_page", default=""), "source": source}
        if head not in index:
            index[head] = len(groups)
            groups.append([head, [rec]])
        else:
            groups[index[head]][1].append(rec)
    return groups


_EVAL_SCORE_CUE_RE = re.compile(r"得\s*\d|满分|\d+\s*分|最多.*分|综合评定|酌情打分")
_EVAL_META_RE = re.compile(
    r"评委评分\s*=|A1\s*[、,＋+].*An|推荐的?中标候选人|^说明$"
)


def _is_eval_shell(text, component):
    """True when item/factor is just the section banner, e.g. 技术部分(F1、满分为100分)."""
    t, c = _clean_text(text), _clean_text(component)
    if not t:
        return True
    if t == c:
        return True
    return bool(c and t.startswith(c) and re.search(r"[（(].*满分", t))


def _eval_detail(it):
    """评分细则：接口的具体内容在 source_text；factor 只是栏目标题时不要用它冒充正文。"""
    factor = _clean_text(_g(it, "factor", default=""))
    source = _clean_text(_g(it, "source_text", default=""))
    item = _clean_text(_g(it, "item", default=""))
    comp = _clean_text(_g(it, "component", default=""))
    if source and (_is_eval_shell(factor, comp) or not factor):
        return source
    if source and factor:
        if _EVAL_SCORE_CUE_RE.search(factor) and len(factor) >= 24:
            return factor
        if len(source) > len(factor) or _EVAL_SCORE_CUE_RE.search(source):
            return source
        return factor
    return factor or source or item


def _is_eval_meta(it):
    """Skip formula / recommendation-method rows that are not scoring criteria."""
    if _EVAL_SCORE_CUE_RE.search(_clean_text(_g(it, "source_text", default=""))):
        return False
    blob = _clean_text(" ".join(str(_g(it, f, default="") or "") for f in ("component", "item", "factor")))
    return bool(_EVAL_META_RE.search(blob))


def _eval_rows(rows):
    """Flatten evaluation[] into table rows: component / item / detail / score / weight."""
    out = []
    for it in rows or []:
        if not isinstance(it, dict) or _is_eval_meta(it):
            continue
        comp = _clean_text(_g(it, "component", default="")) or "其他"
        item = _clean_text(_g(it, "item", default=""))
        if _is_eval_shell(item, comp):
            item = ""
        out.append({
            "component": comp,
            "item": item,
            "detail": _eval_detail(it),
            "score": _g(it, "score"),
            "weight": _g(it, "weight"),
            "page": _g(it, "source_page", default=""),
        })
    return out


def _project_name(pinfo):
    for it in pinfo or []:
        if not isinstance(it, dict):
            continue
        if _g(it, "field_name") in ("项目名称", "招标项目名称", "采购项目名称"):
            name = _clean_text(_g(it, "field_value", default=""))
            if name:
                return name
    return ""


def _ev(obj):
    """证据多形态归一：兼容 {excerpt}/{text}/{field,expected_text} 及 JSON 字符串。"""
    obj = _as_struct(obj)
    if not isinstance(obj, dict):
        text = _clean_text(obj)
        return "" if _is_blank(text) else text
    excerpt = ""
    for k in ("excerpt", "text", "requirement_excerpt", "bid_excerpt"):
        if obj.get(k):
            excerpt = _clean_text(obj[k])
            break
    loc = obj.get("section_path") or obj.get("section_title") or obj.get("page")
    if isinstance(loc, list):
        loc = " / ".join(_clean_text(x) for x in loc if _clean_text(x))
    elif loc not in (None, ""):
        loc = _clean_text(loc)
    else:
        loc = ""
    if excerpt:
        return f"{excerpt}（{loc}）" if loc else excerpt
    if obj.get("field") or obj.get("expected_text"):
        return f"{_clean_text(obj.get('field', ''))}：{_clean_text(obj.get('expected_text', ''))}".strip("：")
    terms = obj.get("matched_terms")
    if isinstance(terms, list):
        hit = "、".join(_clean_text(t) for t in terms[:8] if _clean_text(t))
        if hit:
            return f"命中：{hit}"
    return ""


_DUP_CAT_ZH = {
    "table": "表格结构", "semantic": "语义相似", "metadata": "文档属性",
    "image": "图片相似", "text": "文本重复",
}
_DUP_STRENGTH_ZH = {"strong": "强", "medium": "中", "weak": "弱"}
_DUP_ROLE_ZH = {
    "required_form": "制式表格", "commercial": "商务", "technical": "技术",
    "pricing": "报价", "qualification": "资格", "attachment": "附件",
    "other": "其他", "unclassified": "未分类",
}
_DUP_META_ZH = {
    "author": "作者", "creator": "作者", "last_modified_by": "最后修改人",
    "company": "文档公司", "template": "模板标识", "template_id": "模板 ID",
    "revision_id": "修订痕迹", "style_fingerprint": "样式指纹",
    "embedded_object_paths": "嵌入对象路径", "created_at": "创建时间",
    "modified_at": "修改时间", "document_simhash": "文档指纹",
}


def _pretty_meta_value(value):
    s = _clean_text(value)
    if len(s) >= 16 and s[4:5] == "-" and "T" in s[:20]:
        return s[:10] + " " + s[11:16]
    return s


def _loc_label(loc):
    if not isinstance(loc, dict):
        return "", ""
    if loc.get("metadata_key"):
        raw = _clean_text(loc.get("metadata_key"))
        return _DUP_META_ZH.get(raw, raw), _pretty_meta_value(loc.get("value") or "")
    title = _clean_text(
        loc.get("title") or loc.get("section_title") or loc.get("expected_entity") or "")
    value = _clean_text(loc.get("value") or loc.get("matched_text") or "")
    return title, value


def _dup_evidence_note(evidence):
    """把查重 evidence 对象收成一句人话，绝不输出 JSON。"""
    ev = _as_struct(evidence)
    if not isinstance(ev, dict) or not ev:
        return ""
    a = ev.get("file_a_location") if isinstance(ev.get("file_a_location"), dict) else {}
    b = ev.get("file_b_location") if isinstance(ev.get("file_b_location"), dict) else {}
    parts = []
    ta, va = _loc_label(a)
    tb, vb = _loc_label(b)
    kind = "属性" if (a.get("metadata_key") or b.get("metadata_key")) else "位置"
    if ta and tb and ta == tb:
        parts.append(f"{kind}：{ta}")
    elif ta or tb:
        parts.append(f"{kind}：" + " ↔ ".join(x for x in (ta, tb) if x))
    if va and vb and va == vb:
        parts.append(f"取值：{va}")
    elif va or vb:
        parts.append("取值：" + " / ".join(x for x in (va, vb) if x))
    headers = a.get("matched_headers") or ev.get("matched_headers")
    if isinstance(headers, list) and headers:
        parts.append("表头：" + "、".join(str(h) for h in headers[:6]))
    src = a if a else ev
    for label, key in (
        ("语义", "semantic_cosine"), ("用词", "tfidf_cosine"),
        ("重叠", "jaccard_similarity"), ("指纹", "simhash_similarity"),
        ("表头相似", "header_similarity"),
    ):
        if src.get(key) not in (None, "", 0, 0.0):
            parts.append(f"{label} {_pct(src.get(key))}")
    return "；".join(parts)


def _sim_score(value):
    try:
        n = float(value)
    except (TypeError, ValueError):
        return str(value or "-")
    if 0 <= n <= 1:
        return _pct(n)
    return str(value)


def _pct(value):
    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return "-"


def _filesize(value):
    try:
        n = int(value)
    except (TypeError, ValueError):
        return "-"
    if n >= 1024 * 1024 * 1024:
        return f"{n / 1024 / 1024 / 1024:.2f} GB"
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.1f} MB"
    if n >= 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n} B"


def _short_json(value, limit=220):
    if value in (None, "", [], {}):
        return ""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False)
    else:
        text = str(value)
    return text if len(text) <= limit else text[:limit] + "..."


def _semantic_review_lines(summary):
    """把合规语义审查状态转成总览区可读文案。"""
    if not isinstance(summary, dict):
        return []
    lines = []
    phase = _g(summary, "conclusion_phase", default="")
    overview_ready = _g(summary, "overview_ready", default=None)
    semantic = _g(summary, "semantic_review", default={}) or {}
    state = _g(semantic, "state", default="")
    state_label = _SEMANTIC_STATE_ZH.get(str(state).strip(), str(state).strip()) if state else ""
    phase_label = _SEMANTIC_STATE_ZH.get(str(phase).strip(), str(phase).strip()) if phase else ""
    if state_label:
        lines.append(f"语义审查状态：{state_label}")
    if phase_label and phase_label != state_label:
        lines.append(f"结论阶段：{phase_label}")
    if overview_ready is not None:
        lines.append(f"总览状态：{'可用' if bool(overview_ready) else '未完整生成'}")
    msg = _g(semantic, "message_zh", default="") or _g(semantic, "message", default="")
    if msg:
        lines.append(str(msg))
    return lines


def _partial_summary_items(partial):
    """兼容字段可能漂移的 partial_summary，只展示短值，跳过复杂嵌套。"""
    if not isinstance(partial, dict) or not partial:
        return []
    labels = {
        "high_count": "高风险",
        "review_count": "待复核",
        "tip_count": "提示项",
        "similarity_count": "多文件雷同",
        "manual_unchecked_count": "手动待确认",
        "conclusion": "阶段结论",
        "message": "阶段说明",
        "message_zh": "阶段说明",
        "state": "阶段状态",
        "status": "阶段状态",
        "checked_count": "已检查项",
        "total_count": "总项数",
    }
    items = []
    for key, label in labels.items():
        val = partial.get(key)
        if val in (None, "", [], {}):
            continue
        if key in ("state", "status"):
            val = _SEMANTIC_STATE_ZH.get(str(val).strip(), val)
        items.append(f"{label}：{val}")
    for key, val in partial.items():
        if key in labels or val in (None, "", [], {}):
            continue
        if isinstance(val, (dict, list)):
            continue
        items.append(f"{key}：{val}")
    return items


def _auto_tender_name(service, result):
    if not isinstance(result, dict):
        return None
    for k in ("tender_filename", "original_filename", "filename"):
        if result.get(k):
            return result[k]
    if service == "interpretation":
        for it in (result.get("project_info") or []):
            if isinstance(it, dict) and it.get("field_name") in (
                    "项目名称", "招标项目名称", "采购项目名称") and it.get("field_value"):
                return it["field_value"]
    if service == "compliance":
        body = result.get("compliance") if isinstance(result.get("compliance"), dict) else result
        for item in ((body or {}).get("bid_files") or []):
            if isinstance(item, dict) and item.get("filename"):
                return item["filename"]
    if service == "bid_duplicate":
        body = result.get("duplicate") if isinstance(result.get("duplicate"), dict) else result
        names = [
            item.get("filename") for item in ((body or {}).get("files") or [])
            if isinstance(item, dict) and item.get("role") != "tender" and item.get("filename")
        ]
        if len(names) >= 2:
            return f"{names[0]} ↔ {names[1]}"
        if names:
            return names[0]
    return None
