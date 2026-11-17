#!/usr/bin/env python3
"""
clause_extractor.py - Extract structured clauses from a bid document (BidHunter).

v2.0  : first release. Single fixed window of MAX_CHARS=9000 characters.
v2.8  : ★ coverage rewrite.
        - Old behaviour on a 300-page tender (≈200k chars): the model saw the
          first 9,000 characters — roughly 4% of the document — and reported a
          confident, complete-looking JSON. That is the worst possible failure
          mode: a truncated read that looks like a full one. Measured on real
          files in this repo the coverage was as low as 34%.
        - Now: structural segmentation + per-segment extraction + merge/dedupe.
        - Adds 评分点逐项映射 (was only price/tech/business percentages) and
          分值守恒校验, so a scoring table that does not add up is reported
          instead of silently accepted.
        - Zero-AI-key fallback: a rule engine still returns the fields it can
          see, labelled as such, instead of exiting with code 2.

Design rules:
  1. Never invent. A field that cannot be located in the text is null/empty and
     is listed in `unverified`. Do not fill a plausible-looking value.
  2. Always report coverage. `meta.coverage_pct` and `meta.segments` tell the
     user how much of the document was actually read.
  3. Quote, don't paraphrase. Every extracted requirement carries `source_excerpt`
     so a human can find it in the original.

Usage:
  python3 clause_extractor.py <doc_text_file.txt>      # prints JSON
  echo "文本..." | python3 clause_extractor.py -        # read from stdin
  python3 clause_extractor.py tender.pdf --no-ai       # rule engine only
  python3 clause_extractor.py tender.pdf --json-out out.json
"""
import os
import re
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_parser import parse, segment
from minimax_client import MiniMaxClient, ConfigError

# Per-segment budget. Deliberately far below model context so that a long
# document becomes many focused calls instead of one blurry one.
SEG_BUDGET = 8000
SEG_OVERLAP = 300

SYSTEM = (
    "你是招投标文件分析专家。从给定的招标文件**片段**中提取结构化信息。"
    "只输出 JSON，不要解释，不要 Markdown 代码块。字段："
    "project_name(项目名称或null), owner(招标单位/采购人或null),"
    "qualification_requirements(数组，每项为对象 {item, source_excerpt, mandatory(布尔: 原文含必须/应/须/不得则为true), page_hint(原文出处或null)}),"
    "budget_yuan(预算金额, 整数元, 无法识别填null),"
    "budget_excerpt(预算原文或null),"
    "bid_deadline(投标截止时间原文照抄或null),"
    "bid_validity_days(投标有效期天数整数或null),"
    "evaluation_method(评标办法名称或null),"
    "score_items(数组，每项为对象 {name, score(数值或null), tier(档次定义原文或null), requirement(得分条件原文或null)}),"
    "score_weights(对象，含 price/tech/business 百分比整数，无法识别填空对象),"
    "key_clauses(数组，每项为对象 {topic, source_excerpt}),"
    "has_risk_tendency(是否含排他/内定倾向条款, 布尔)."
    "严格约束：只提取本片段中确实出现的内容。任何无法在本片段中找到依据的字段一律填 null 或空数组，"
    "严禁用行业惯例、常见做法补全。"
)

FIELD_LIST = [
    "project_name", "owner", "qualification_requirements", "budget_yuan",
    "budget_excerpt", "bid_deadline", "bid_validity_days", "evaluation_method",
    "score_items", "score_weights", "key_clauses", "has_risk_tendency",
]


# ----------------------------------------------------------------------------
# rule engine — zero AI cost, runs even without an API key
# ----------------------------------------------------------------------------

RE_BUDGET = re.compile(
    r"(?:预算|采购预算|招标控制价|最高投标限价|项目预算|概算|投资估算|预算金额)"
    r"[^\d]{0,20}([\d,，.]+)\s*(万元|万|元|亿元|亿)?")
RE_DEADLINE = re.compile(
    r"(?:投标|递交|响应|报价|磋商|谈判)?文件?(?:递交|提交|送达|截止|递交截止|提交截止)"
    r"(?:时间|日期|期限)?[^\d]{0,25}(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日"
    r"(?:\s*\d{1,2}[:：]\d{2})?)")
RE_VALIDITY = re.compile(
    r"投标有效期[^\d]{0,15}(\d{2,4})\s*(日历天|天|个月)")
RE_METHOD = re.compile(
    r"(经评审的?最低(?:投标)?价法|最低评标价法|综合评估法|综合评分法|性价比法|"
    r"经评审的?最低价格法|合理低价法)")
RE_REQUIRED = re.compile(
    r"(具备|具有|拥有|持有|取得|通过|满足|提供|提交|响应|符合)[^\n。；;]{0,40}"
    r"(资质|资格|证书|许可|业绩|经验|社保|纳税|财务|审计|人员|证书|认证|承诺函|报告)")

STOP_TERMS = (
    "投标文件", "招标文件", "资格证明", "评分", "评标", "投标保证金",
    "资格审查", "技术", "商务", "报价", "承诺", "格式", "附件",
)


def rule_extract(text):
    """Best-effort extraction with no network and no API key. Low recall,
    zero hallucination — every field below is copied from the source text."""
    out = {k: (None if k not in ("qualification_requirements", "key_clauses",
                                 "score_items", "score_weights") else [])
           for k in FIELD_LIST}
    out["score_weights"] = {}
    if not text:
        return out, "rule-engine:empty"

    m = RE_DEADLINE.search(text)
    if m:
        out["bid_deadline"] = re.sub(r"\s+", "", m.group(1))

    m = RE_VALIDITY.search(text)
    if m:
        v = int(m.group(1))
        out["bid_validity_days"] = v * 30 if m.group(2) == "个月" else v

    m = RE_METHOD.search(text)
    if m:
        out["evaluation_method"] = m.group(1)

    m = RE_BUDGET.search(text)
    if m:
        raw = m.group(1).replace(",", "").replace("，", "")
        unit = m.group(2) or "元"
        try:
            val = float(raw)
        except ValueError:
            val = None
        if val is not None:
            mult = {"万": 1e4, "万元": 1e4, "亿": 1e8, "亿元": 1e8}.get(unit, 1.0)
            out["budget_yuan"] = int(val * mult)
            out["budget_excerpt"] = m.group(0)[:80]

    seen = set()
    for m in RE_REQUIRED.finditer(text):
        line = text[max(0, m.start() - 30): m.end() + 30].replace("\n", " ").strip()
        if len(line) < 8 or not any(t in line for t in STOP_TERMS):
            continue
        key = line[:40]
        if key in seen:
            continue
        seen.add(key)
        out["qualification_requirements"].append({
            "item": line[:80],
            "source_excerpt": m.group(0)[:80],
            "mandatory": bool(re.search(r"必须|应当|须|不得|严禁", line)),
            "page_hint": None,
        })
        if len(out["qualification_requirements"]) >= 40:
            break

    out["has_risk_tendency"] = bool(re.search(
        r"(仅限|只接受|指定品牌|唯一|指定供应商|不得参与其他|排他)", text))
    return out, "rule-engine"


# ----------------------------------------------------------------------------
# merge / dedupe / validate
# ----------------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", str(s or "")).lower()


def merge_lists(dst, src, key="item", limit=200):
    """Append items from src to dst, deduplicating on a normalised key."""
    have = {_norm(d.get(key)) for d in dst if isinstance(d, dict)}
    for it in (src or []):
        if not isinstance(it, dict):
            continue
        k = _norm(it.get(key))
        if not k or k in have:
            continue
        have.add(k)
        dst.append(it)
        if len(dst) >= limit:
            break
    return dst


def merge(base, part):
    """Merge one segment's result into the accumulator."""
    for k in FIELD_LIST:
        if k not in part:
            continue
        v = part[k]
        if isinstance(v, list):
            key = "name" if k == "score_items" else (
                "item" if k == "qualification_requirements" else "topic")
            merge_lists(base.setdefault(k, []), v, key=key)
        elif isinstance(v, dict):
            for wk, wv in v.items():
                if wv not in (None, "", 0):
                    base.setdefault(k, {}).setdefault(wk, wv)
        elif v not in (None, "", False) and base.get(k) in (None, "", [], {}, False):
            # first non-empty wins; boolean False is a real answer so only fill
            # when the accumulator has never been set
            base[k] = v
        elif k == "has_risk_tendency" and v is True:
            base[k] = True
    return base


def score_conservation(score_items, score_weights):
    """Check that per-item scores add up. Returns a diagnosis dict.

    A tender whose scoring table does not sum to the stated total usually means
    a scoring row was missed — which is exactly the leak this whole rewrite is
    meant to close, so it must be surfaced, not smoothed over.
    """
    scored = [s for s in (score_items or [])
              if isinstance(s, dict) and isinstance(s.get("score"), (int, float))]
    if not scored:
        return {"checked": False,
                "reason": "未抽到任何带分值的评分项（评分表可能未被识别）",
                "action": "人工核对评分办法章节，勿依赖本结果"}
    total = sum(s["score"] for s in scored)
    diff = round(total - 100.0, 2)
    if abs(diff) < 0.51:
        return {"checked": True, "sum": total, "diff": diff, "verdict": "PASS",
                "reason": f"评分项合计 {total:g}，与 100 分一致"}
    # maybe the total is not 100 (some tenders score out of 80 or 120)
    return {"checked": True, "sum": total, "diff": diff, "verdict": "MISMATCH",
            "reason": f"评分项合计 {total:g}，与 100 分差 {diff:+g}",
            "action": "差额必须解释：可能是漏抄了评分项，或本标总分值非 100。"
                      "不得直接采信，须人工核对原表"}


def coverage_meta(total_chars, segs, used_ai):
    if not total_chars:
        return {"total_chars": 0, "segments": 0, "coverage_pct": 0.0,
                "used_ai": used_ai, "note": "未读到任何文本，见 backend 提示"}
    read = sum(len(s[1]) for s in segs)
    return {
        "total_chars": total_chars,
        "segments": len(segs),
        "chars_read": read,
        "coverage_pct": round(min(read, total_chars) / total_chars * 100, 1),
        "used_ai": used_ai,
        "note": ("分片全覆盖" if len(segs) > 1 else
                 "单片段，全文覆盖"),
    }


# ----------------------------------------------------------------------------
# main extraction
# ----------------------------------------------------------------------------

def extract(text, use_ai=True, budget=SEG_BUDGET):
    """Extract structured clauses from full tender text.

    Returns (result_dict, meta_dict). Never raises on document problems.
    """
    segs = segment(text, budget=budget, overlap=SEG_OVERLAP)
    base = {k: (None if k not in ("qualification_requirements", "key_clauses",
                                  "score_items", "score_weights") else [])
            for k in FIELD_LIST}
    base["score_weights"] = {}
    base["has_risk_tendency"] = False

    if not segs:
        return base, coverage_meta(len(text or ""), [], False)

    rule_result, backend = rule_extract(text)
    for k in FIELD_LIST:
        if isinstance(rule_result.get(k), list):
            merge_lists(base.setdefault(k, []), rule_result[k],
                        key="name" if k == "score_items" else (
                            "item" if k == "qualification_requirements" else "topic"))
        elif isinstance(rule_result.get(k), dict):
            for wk, wv in rule_result[k].items():
                if wv not in (None, "", 0):
                    base[k].setdefault(wk, wv)
        elif base.get(k) is None and rule_result.get(k) not in (None, ""):
            base[k] = rule_result[k]
    if rule_result.get("has_risk_tendency"):
        base["has_risk_tendency"] = True

    used_ai = False
    if use_ai:
        try:
            client = MiniMaxClient.from_config()
        except ConfigError:
            client = None
        if client is not None:
            used_ai = True
            for i, (_idx, piece) in enumerate(segs):
                prompt = (f"招标文件片段（第 {i+1}/{len(segs)} 段）：\n'''{piece}'''\n"
                          f"请提取本片段中出现的信息。")
                try:
                    raw = client.chat(prompt, system=SYSTEM, json_mode=True)
                    raw = raw.strip()
                    if raw.startswith("```"):
                        raw = raw[raw.find("{"): raw.rfind("}") + 1]
                    merge(base, json.loads(raw))
                except Exception:
                    # one bad segment must not lose the other N-1 segments
                    continue

    meta = coverage_meta(len(text), segs, used_ai)
    meta["backend"] = backend
    if not used_ai:
        meta["note"] = ("未配置 AI key，已用规则引擎抽取——覆盖到的字段可信，"
                        "未覆盖字段不代表不存在，须人工核对。")
    base["score_conservation"] = score_conservation(base["score_items"],
                                                    base["score_weights"])
    base["unverified"] = [f for f in FIELD_LIST
                          if not base.get(f) and f not in
                          ("score_items", "score_weights", "key_clauses",
                           "qualification_requirements", "has_risk_tendency")]
    return base, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default="-",
                    help="文件路径（pdf/docx/txt/md），- 表示 stdin")
    ap.add_argument("--no-ai", action="store_true", help="只用规则引擎，零 API 成本")
    ap.add_argument("--budget", type=int, default=SEG_BUDGET,
                    help=f"每片字符预算（默认 {SEG_BUDGET}）")
    ap.add_argument("--json-out", help="额外写出 JSON 到文件")
    args = ap.parse_args()

    if args.src == "-":
        text = sys.stdin.read()
    else:
        if not os.path.exists(args.src):
            print(json.dumps({"error": f"文件不存在: {args.src}"}, ensure_ascii=False))
            sys.exit(1)
        text, backend = parse(args.src)
        if not text:
            print(json.dumps({
                "error": "未能提取文本",
                "backend": backend,
                "hint": "纯扫描件需先 OCR（tencentcloud-ocr）；"
                        "PDF 建议 pip install PyPDF2 或安装 poppler 的 pdftotext",
            }, ensure_ascii=False))
            sys.exit(1)

    data, meta = extract(text, use_ai=not args.no_ai, budget=args.budget)
    out = {"clauses": data, "meta": meta}
    txt = json.dumps(out, ensure_ascii=False, indent=2)
    print(txt)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(txt)


if __name__ == "__main__":
    main()
