#!/usr/bin/env python3
"""
qual_check.py - Qualification matching engine for BidHunter v1.1.
No third-party dependencies. Uses Python standard library only.

Usage:
  python3 qual_check.py <cache_file.jsonl> <rules_file.json>
  Output: JSON lines to stdout, each with qualification verdict.

  python3 qual_check.py --validate-rules <rules_file.json>
  Output: rule health check result to stderr.
"""

import json
import sys
import os
import re
from datetime import datetime


def log(msg):
    """Print log message to stderr with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


def load_rules(rules_path):
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_announcements(cache_path):
    announcements = []
    if not os.path.exists(cache_path):
        return announcements
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                announcements.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return announcements


def _is_cjk(char):
    """Check if a character is a CJK (Chinese) character."""
    cp = ord(char)
    # CJK Unified Ideographs + Extension + Compatibility
    return 0x4E00 <= cp <= 0x9FFF or \
           0x3400 <= cp <= 0x4DBF or \
           0x20000 <= cp <= 0x2A6DF


def smart_match(text, keyword, exclude_context=None):
    """
    Boundary-aware keyword match for Chinese text.
    - Left boundary: keyword must not be preceded by a CJK character
      (avoids matching '电气' as a substring of '新电气石')
    - Right boundary: if the keyword is followed by a CJK character,
      the CJK run must be >= 2 chars (keyword is standalone, not a 1-char suffix compound)
      (avoids matching '电气' in '电气石' (suffix '石'=1char), but allows '电气设备' (suffix '设备'>=2))
    - exclude_context: if any exclude pattern appears anywhere in the text, reject match
    Returns True if matched, False otherwise.
    """
    if not keyword or not text:
        return False

    escaped = re.escape(keyword)
    pattern = re.compile(escaped)
    m = pattern.search(text)
    if not m:
        return False

    start, end = m.start(), m.end()

    # Left boundary check: preceding char must not be CJK
    if start > 0 and _is_cjk(text[start - 1]):
        return False

    # Right boundary check: if next char is CJK, count the full CJK run
    if end < len(text) and _is_cjk(text[end]):
        # Count how many consecutive CJK chars follow
        run = 0
        for i in range(end, len(text)):
            if _is_cjk(text[i]):
                run += 1
            else:
                break
        # If CJK run is exactly 1 char, keyword is a 1-char suffix compound → block
        if run == 1:
            return False
        # run >= 2: keyword is followed by a word (e.g. "电气设备"), allow

    # Context exclusion: if any exclude pattern found in text, reject
    if exclude_context:
        for ctx in exclude_context:
            if ctx in text:
                return False

    return True


def validate_rules(rules_path):
    """
    Check rule library health.
    Prints issues to stderr. Returns True if passed, False if issues found.
    """
    log(f"Validating rules: {rules_path}")
    issues = []
    warnings = []

    try:
        rules = load_rules(rules_path)
    except Exception as e:
        issues.append(f"Failed to load rules: {e}")
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return False

    # 1. Check each entity has non-empty capabilities
    entities = rules.get("entities", {})
    if not entities:
        issues.append("No entities defined.")
    else:
        for eid, edata in entities.items():
            caps = edata.get("capabilities", [])
            if not caps:
                issues.append(f"Entity '{eid}' has empty capabilities list.")
            # Check for duplicate keywords
            if len(caps) != len(set(caps)):
                seen = set()
                dupes = []
                for c in caps:
                    if c in seen:
                        dupes.append(c)
                    seen.add(c)
                issues.append(f"Entity '{eid}' has duplicate capability keywords: {dupes}")

    # 2. Check capability keywords vs red_alerts conflict
    red_alerts = set(rules.get("red_alerts", []))
    if entities:
        for eid, edata in entities.items():
            caps = set(edata.get("capabilities", []))
            conflict = caps & red_alerts
            if conflict:
                issues.append(
                    f"Entity '{eid}': capability keywords conflict with red_alerts: {sorted(conflict)}"
                )

    # 3. Check special_rules have required fields
    for rule in rules.get("special_rules", []):
        # 空 match_keywords 是合法的"不触发"哨兵，仅警告不阻断
        if not rule.get("match_keywords"):
            warnings.append(f"Special rule '{rule.get('id', '?')}' has empty match_keywords (will never trigger; fill to enable).")
        if not rule.get("action"):
            issues.append(f"Special rule '{rule.get('id', '?')}' missing action.")

    # 4. Check red_alerts no duplicates
    if len(rules.get("red_alerts", [])) != len(red_alerts):
        issues.append("red_alerts list contains duplicate entries.")

    if issues:
        for w in warnings:
            print(f"NOTE: {w}", file=sys.stderr)
        for issue in issues:
            print(f"WARNING: {issue}", file=sys.stderr)
        log(f"Rule validation FAILED ({len(issues)} issue(s) found)")
        return False
    else:
        for w in warnings:
            print(f"NOTE: {w}", file=sys.stderr)
        log("Rule validation passed.")
        return True


def check_service_type_gate(title, gate):
    """
    v1.2 服务类型门禁 —— 采购标的的【服务类型】优先于项目名里的动词关键词。

    背景（2026-09-11 案例 614535）：『销售公司东莞公司楼宇安全整治维修改造项目监理服务』
    真正的标的是【监理服务】，"维修改造"只是修饰语。按项目名动词命中"维修能力"= 误判可投。

    ⚠️ 本函数刻意使用【纯子串匹配】而非 smart_match ——
    因为 smart_match 的左边界规则（关键词前一字符不得为 CJK）导致
    出现在标题中部的词（监理/消防/电梯…）永远匹配不到，这是系统性漏判源。

    gate 结构：
      {"blocked_types": {"监理": {"keywords": ["监理"], "action": "not_investable", "reason": "..."}}}
    """
    if not title or not gate:
        return None
    for type_name, cfg in (gate.get("blocked_types") or {}).items():
        for kw in (cfg.get("keywords") or []):
            if kw and kw in title:
                return {
                    "verdict": cfg.get("action", "needs_review"),
                    "reason": f"{cfg.get('reason', '')}〔服务类型门禁：{type_name}，命中「{kw}」〕",
                    "gate_type": type_name,
                }
    return None


def check_substring_alerts(title, substring_alerts):
    """
    v1.2 子串红警 —— 不依赖边界规则的强制拦截词表。

    用于 smart_match 左边界规则会漏掉的高风险资质词（出现在标题中部时）。
    例："某厂消防设施改造" → "消防"前是"厂"(CJK) → smart_match 漏判。
    本函数用纯 in 判断，命中即拦。
    """
    if not title or not substring_alerts:
        return None
    # 兼容两种写法：["监理", ...] 或 {"_list": ["监理", ...], "_note": "..."}
    if isinstance(substring_alerts, dict):
        substring_alerts = substring_alerts.get("_list", []) or []
    for alert in substring_alerts:
        if alert and alert in title:
            return {"verdict": "not_investable", "reason": f"红色预警（子串）：{alert}"}
    return None


def check_special_rules(title, special_rules):
    """Check special rules first (highest priority)."""
    for rule in special_rules:
        keywords = rule.get("match_keywords", [])
        for kw in keywords:
            if smart_match(title, kw):
                return {
                    "verdict": rule.get("action", "unknown"),
                    "reason": rule.get("description", ""),
                    "assigned_entity": rule.get("assigned_entity", ""),
                    "rule_id": rule.get("id", ""),
                }
    return None


def check_red_alerts(title, red_alerts, exclude_contexts=None):
    """
    Check if title contains any red-alert keywords (boundary-aware).
    exclude_contexts: dict mapping alert -> list of disqualifying context patterns
    """
    if exclude_contexts is None:
        exclude_contexts = {}

    for alert in red_alerts:
        ctx = exclude_contexts.get(alert)
        if smart_match(title, alert, exclude_context=ctx):
            return {"verdict": "not_investable", "reason": f"红色预警：{alert}"}
    return None


def match_entity(title, entities, exclude_contexts=None, loose=False):
    """
    Match title against entity capabilities (boundary-aware).
    Returns best matching entity.

    loose=True (v1.2): 使用纯子串匹配，绕过 smart_match 的 CJK 左边界限制。
    为什么需要：左边界规则（关键词前一字符不得为 CJK）导致出现在标题中部的
    能力词（如"…零星维修服务"里的"维修"）永远匹配不到 → 大量该投的标被误判
    为「需确认」。对【能力词】而言漏判代价高于误判代价（宁可多看几条），
    故提供宽松模式；假阳性仍可用 _exclude_contexts 过滤。
    """
    if exclude_contexts is None:
        exclude_contexts = {}

    best_entity = None
    best_score = 0
    for entity_id, entity_data in entities.items():
        capabilities = entity_data.get("capabilities", [])
        score = 0
        matched_caps = []
        for cap in capabilities:
            ctx = exclude_contexts.get(cap)
            if loose:
                hit = bool(cap) and (cap in title)
                if hit and ctx and any(c in title for c in ctx):
                    hit = False
            else:
                hit = smart_match(title, cap, exclude_context=ctx)
            if hit:
                score += 1
                matched_caps.append(cap)
        if score > best_score:
            best_score = score
            best_entity = {
                "entity_id": entity_id,
                "entity_name": entity_data.get("name", entity_id),
                "matched_capabilities": matched_caps,
                "score": score,
            }
    return best_entity


def check_skip_result(title, skip_keywords):
    """Check if this is a result announcement (not a bid invitation)."""
    for kw in skip_keywords:
        if smart_match(title, kw):
            return True
    return False


def classify_region(title, region_priority):
    """Check if title mentions a high-priority region."""
    high_regions = region_priority.get("high", [])
    for region in high_regions:
        if region in title:
            return {"is_priority": True, "region": region}
    return {"is_priority": False, "region": ""}


def _extract_budget(title):
    """Extract budget from title text. Returns int (CNY yuan) or None.
    Supports 亿元 / 万元 patterns common in Chinese bid notices."""
    if not title:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*亿元", title)
    if m:
        return int(float(m.group(1)) * 10**8)
    m = re.search(r"(\d+(?:\.\d+)?)\s*万元", title)
    if m:
        return int(float(m.group(1)) * 10**4)
    return None


def _industry_of(matched_caps, rules):
    """Map matched capability keywords to an industry category via rules mapping."""
    mapping = rules.get("industry_categories", {}) or {}
    cats = set()
    for cap in (matched_caps or []):
        for cat, kws in mapping.items():
            if cap in kws:
                cats.add(cat)
    if not cats:
        return ""
    return "/".join(sorted(cats))


def compute_match_score(ann, rules):
    """
    Compute a 0-100 investability score (A1).
    Components: capability hits (≤40) + region priority (≤20) +
    industry fit (≤15) + budget fit (≤15) - needs_review penalty (25).
    Returns {score, breakdown, level, industry, budget}.
    """
    title = ann.get("title", "")
    verdict = ann.get("verdict", "")
    breakdown = {}
    score = 0

    if verdict in ("not_investable", "skip"):
        return {"score": 0, "breakdown": {"verdict": "不可投/跳过"},
                "level": "不可投", "industry": "", "budget": None}

    matched = ann.get("matched_capabilities", []) or []
    cap_score = min(len(matched) * 12, 40)
    breakdown["capability"] = cap_score
    score += cap_score

    region_info = ann.get("region_info", {}) or {}
    breakdown["region"] = 20 if region_info.get("is_priority") else 0
    score += breakdown["region"]

    industry = _industry_of(matched, rules)
    industry_priority = rules.get("industry_priority", []) or []
    breakdown["industry"] = 15 if (industry and industry in industry_priority) else 0
    score += breakdown["industry"]

    budget = _extract_budget(title)
    budget_range = rules.get("budget_priority", {}) or {}
    lo, hi = budget_range.get("min"), budget_range.get("max")
    if budget is not None and lo is not None and hi is not None:
        breakdown["budget"] = 15 if (lo <= budget <= hi) else 0
    else:
        breakdown["budget"] = 0
    score += breakdown["budget"]

    if verdict == "needs_review":
        score = max(score - 25, 0)
        breakdown["needs_review"] = -25

    score = max(0, min(100, score))

    if verdict == "investable":
        level = ("强烈推荐" if score >= 80 else
                 "建议跟" if score >= 55 else "可投(一般)")
    elif verdict == "needs_review":
        level = "需确认"
    else:
        level = "不可投"

    return {"score": score, "breakdown": breakdown, "level": level,
            "industry": industry, "budget": budget}


def evaluate_announcement(ann, rules):
    """Main evaluation function. Returns verdict dict (v1.5: +score/industry/budget)."""
    title = ann.get("title", "")

    # Load exclude contexts if present in rules
    exclude_contexts = rules.get("_exclude_contexts", {})

    base = {
        "score": 0,
        "score_breakdown": {},
        "score_level": "—",
        "industry": "",
        "budget": None,
        "region_info": classify_region(title, rules.get("region_priority", {})),
    }

    # Skip result announcements
    if check_skip_result(title, rules.get("skip_keywords_result", [])):
        return {
            **ann, **base,
            "verdict": "skip",
            "reason": "结果/中标公示，非投标公告",
            "assigned_entity": "",
            "matched_capabilities": [],
            "score_level": "跳过",
        }

    # 1. Service-type gate (v1.2, substring) —— 标的服务类型优先于项目名动词
    gate = check_service_type_gate(title, rules.get("service_type_gate", {}))
    if gate:
        return {
            **ann, **base,
            "verdict": gate["verdict"],
            "reason": gate["reason"],
            "assigned_entity": "",
            "matched_capabilities": [],
            "score_level": "服务类型门禁",
        }

    # 1.5 Substring red alerts (v1.2) —— 不受 CJK 边界限制的强制拦截
    sub = check_substring_alerts(title, rules.get("substring_alerts", []))
    if sub:
        return {
            **ann, **base,
            "verdict": sub["verdict"],
            "reason": sub["reason"],
            "assigned_entity": "",
            "matched_capabilities": [],
            "score_level": "不可投",
        }

    # 2. Special rules (highest priority)
    special = check_special_rules(title, rules.get("special_rules", []))
    if special:
        return {
            **ann, **base,
            "verdict": special["verdict"],
            "reason": special["reason"],
            "assigned_entity": special.get("assigned_entity", ""),
            "matched_capabilities": [],
            "score_level": "覆盖规则",
        }

    # 2. Red alerts (boundary-aware)
    red = check_red_alerts(title, rules.get("red_alerts", []), exclude_contexts=exclude_contexts)
    if red:
        return {
            **ann, **base,
            "verdict": red["verdict"],
            "reason": red["reason"],
            "assigned_entity": "",
            "matched_capabilities": [],
            "score_level": "不可投",
        }

    # 3. Entity capability match (boundary-aware; loose mode bypasses CJK boundary)
    loose = bool(rules.get("_match_loose", False))
    entity = match_entity(title, rules.get("entities", {}), exclude_contexts=exclude_contexts, loose=loose)
    if entity:
        result = {
            **ann, **base,
            "verdict": "investable",
            "reason": f"主体能力匹配：{', '.join(entity['matched_capabilities'])}",
            "assigned_entity": entity["entity_id"],
            "assigned_entity_name": entity["entity_name"],
            "matched_capabilities": entity["matched_capabilities"],
        }
        si = compute_match_score(result, rules)
        result.update({"score": si["score"], "score_breakdown": si["breakdown"],
                       "score_level": si["level"], "industry": si["industry"],
                       "budget": si["budget"]})
        return result

    # 4. No match - needs confirmation
    result = {
        **ann, **base,
        "verdict": "needs_review",
        "reason": "未匹配到主体能力词，需人工研判",
        "assigned_entity": "",
        "matched_capabilities": [],
    }
    si = compute_match_score(result, rules)
    result.update({"score": si["score"], "score_breakdown": si["breakdown"],
                   "score_level": si["level"], "industry": si["industry"],
                   "budget": si["budget"]})
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage:", file=sys.stderr)
        print("  python3 qual_check.py --validate-rules <rules_file.json>", file=sys.stderr)
        print("  python3 qual_check.py <cache_file.jsonl> <rules_file.json>", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--validate-rules":
        if len(sys.argv) < 3:
            print("Usage: python3 qual_check.py --validate-rules <rules_file.json>", file=sys.stderr)
            sys.exit(1)
        ok = validate_rules(sys.argv[2])
        sys.exit(0 if ok else 1)

    if len(sys.argv) < 3:
        print("Usage: python3 qual_check.py <cache_file.jsonl> <rules_file.json>", file=sys.stderr)
        sys.exit(1)

    cache_path = sys.argv[1]
    rules_path = sys.argv[2]

    log(f"Loading rules from {rules_path}")
    rules = load_rules(rules_path)
    log(f"Loading announcements from {cache_path}")
    announcements = load_announcements(cache_path)
    log(f"Processing {len(announcements)} announcements")

    verdict_map = {
        "investable": "investable",
        "not_investable": "not_investable",
        "needs_review": "needs_review",
        "skip": "skip",
        "unknown": "needs_review",
    }

    stats = {"investable": 0, "not_investable": 0, "needs_review": 0, "skip": 0}

    for ann in announcements:
        result = evaluate_announcement(ann, rules)
        verdict = verdict_map.get(result["verdict"], "needs_review")
        stats[verdict] = stats.get(verdict, 0) + 1
        result["verdict"] = verdict
        print(json.dumps(result, ensure_ascii=False))

    # Summary to stderr
    total = sum(stats.values())
    log(f"Done. Total: {total} | can: {stats['investable']} | cannot: {stats['not_investable']} | review: {stats['needs_review']} | skip: {stats['skip']}")


if __name__ == "__main__":
    main()
