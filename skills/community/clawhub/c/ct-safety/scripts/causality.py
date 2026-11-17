#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
causality.py / Naranjo 因果归因推理层 (P0-A)

定性补充层：用经典 Naranjo 7 准则对单个药物-事件组合（或单条 FAERS 病例）
做**因果归因（causality）**启发式打分，区分 drug-specific / class-wide /
confounding 的定性线索，作为 disproportionality 统计信号的定性旁证。

关键边界（务必遵守）：
  * 本模块是**纯启发式、定性、non-definitive** 的补充，**不与** PRR / ROR /
    IC / EBGM 等 disproportionality 统计信号混算，也**不喂入**任何统计方法。
  * 输出文案一律用"提示 / 可能 / 建议复核"，**绝不声称因果证明**。
  * 纯标准库实现，无第三方依赖；可独立于主流程运行（见 __main__）。

Naranjo 7 准则（每条给 +1 / 0 / -1）：
  1. 既往反应史 previous_report        —— 是否有既往明确报告（支持性）
  2. 急性发作 acute_onset              —— 事件是否在用药后出现（支持性）
  3. 停药后好转 dechallenge            —— 停药/拮抗后是否好转（支持性）
  4. 再用药复发 rechallenge            —— 再用药是否复发（支持性）
  5. 其他非药物原因 alternative_cause  —— 是否有其他非药物原因（反向：有=-1）
  6. 已知反应模式 known_reaction_pattern —— 是否为该药/同类已知反应（支持性）
  7. 客观证据 objective_evidence       —— 是否有客观证据（实验室/血药浓度/对照）（支持性）

总分判定（经典 Naranjo 7 项适配切点；经典 10 项量表 Definite>=9，此处按 7 项等比
缩放，确保四档均可达）：
  >= 6  : Definite   肯定
  4..5  : Probable    很可能
  1..3  : Possible    可能
  <= 0  : Doubtful   可疑/不大可能
"""
import argparse
import json
import sys

# ---------------------------------------------------------------------------
# 准则定义：polarity "support" => yes=+1 / no=-1 / unknown=0
#          polarity "reverse" =>  yes=-1 / no=+1 / unknown=0（如"存在其他非药物原因"）
# ---------------------------------------------------------------------------
CRITERIA = [
    {"key": "previous_report", "zh": "既往反应史",
     "en": "Previous conclusive reports", "polarity": "support",
     "q": "是否有既往明确报告支持该药-事件关联？"},
    {"key": "acute_onset", "zh": "急性发作",
     "en": "Acute onset after drug", "polarity": "support",
     "q": "不良事件是否在可疑药给药后出现？"},
    {"key": "dechallenge", "zh": "停药后好转",
     "en": "Improvement after dechallenge", "polarity": "support",
     "q": "停药或给予特异性拮抗后反应是否好转？"},
    {"key": "rechallenge", "zh": "再用药复发",
     "en": "Relapse on rechallenge", "polarity": "support",
     "q": "再次给药后反应是否复发？"},
    {"key": "alternative_cause", "zh": "其他非药物原因",
     "en": "Alternative non-drug causes", "polarity": "reverse",
     "q": "是否存在可单独导致该反应的其他非药物原因？"},
    {"key": "known_reaction_pattern", "zh": "已知反应模式",
     "en": "Known reaction pattern", "polarity": "support",
     "q": "该反应是否为该药/同类的已知反应模式（如标签已收录）？"},
    {"key": "objective_evidence", "zh": "客观证据",
     "en": "Objective evidence", "polarity": "support",
     "q": "是否有客观证据（实验室/血药浓度/安慰剂对照等）支持？"},
]

CLASSIFICATION = [
    (6, "Definite", "肯定", "总分 >= 6：因果关联肯定（7 项适配切点；仍是自发报告启发式，非 RCT 证据）"),
    (4, "Probable", "很可能", "总分 4–5：因果关联很可能"),
    (1, "Possible", "可能", "总分 1–3：因果关联可能"),
    (0, "Doubtful", "可疑/不大可能", "总分 <= 0：因果关联可疑或不大可能"),
]


def _encode(val, polarity):
    """Normalize an arbitrary user input into {-1, 0, +1}.

    Accepts: int in {-1,0,1}; str keywords (yes/no/unknown and FAERS-style
    dechallenge/rechallenge tokens); bool. Missing / unknown -> 0 (safe default).
    """
    if val is None:
        return 0
    if isinstance(val, bool):
        v = 1 if val else -1
    elif isinstance(val, (int, float)):
        v = int(val)
        if v not in (-1, 0, 1):
            # out-of-range integers clamp to nearest valid support/contrary
            v = 1 if v > 0 else (-1 if v < 0 else 0)
    else:
        s = str(val).strip().lower()
        if s in ("-1", "no", "n", "否", "not", "absent", "contradictory",
                 "not_recovered", "not_recur", "not_recurred"):
            v = -1
        elif s in ("1", "yes", "y", "是", "recovered", "recovering",
                   "recurred", "recur", "present", "supportive", "positive"):
            v = 1
        elif s in ("0", "unknown", "u", "未知", "?", "na", "none", "null", ""):
            v = 0
        else:
            # unrecognized keyword -> treat as unknown (conservative)
            v = 0
    # reverse polarity flips support/contradictory
    if polarity == "reverse":
        v = -v
    return v


def score_criteria(evidence):
    """Score all 7 criteria from an evidence dict.

    `evidence` maps each criterion key to a raw value (int/-1,0,1, yes/no/unknown,
    or FAERS-style token). Missing keys default to unknown (0). Returns a list of
    per-criterion dicts {key, zh, en, raw, score, polarity} and the total.
    """
    scored = []
    for c in CRITERIA:
        raw = evidence.get(c["key"])
        sc = _encode(raw, c["polarity"])
        scored.append({
            "key": c["key"], "zh": c["zh"], "en": c["en"],
            "question": c["q"], "polarity": c["polarity"],
            "raw": raw, "score": sc,
        })
    total = sum(x["score"] for x in scored)
    return scored, total


def classify(total):
    """Map a total Naranjo score to (code, zh_label, note)."""
    for threshold, code, zh, note in CLASSIFICATION:
        if total >= threshold:
            return code, zh, note
    # fallback (should not happen given the <=0 bucket)
    return "Doubtful", "可疑/不大可能", CLASSIFICATION[-1][3]


def naranjo_assessment(evidence, meta=None):
    """Full assessment for a single drug-event evidence dict.

    Returns a dict: {criteria:[...], total, category_code, category_zh,
    category_note, non_causal:True, mixed_with_disproportionality:False, meta}.
    """
    scored, total = score_criteria(evidence)
    code, zh, note = classify(total)
    return {
        "criteria": scored,
        "total": total,
        "category_code": code,
        "category_zh": zh,
        "category_note": note,
        # 显式声明边界，供报告文案直接引用，避免因果过度声称
        "non_causal": True,
        "mixed_with_disproportionality": False,
        "meta": meta or {},
    }


# ---------------------------------------------------------------------------
# 从 FAERS 病例级记录映射（输入为简单 dict，字段缺失即兜底 unknown=0）
# ---------------------------------------------------------------------------
def from_faers_case(case):
    """Map one FAERS-style case dict to the 7-criterion evidence dict.

    Recognized fields (all optional; missing -> unknown):
      prior_history          : 既往是否明确报告过该反应 (yes/no/unknown)
      onset_after_drug        : 事件是否在用药后出现 (yes/no/unknown)
      dechallenge             : 停药后反应 (recovered/recovering -> 支持;
                                not_recovered -> 反对; unknown/None -> 未知)
      rechallenge             : 再用药反应 (recurred -> 支持; not_recurred/no ->
                                反对; unknown/None -> 未知)
      alternative_cause       : 是否存在其他非药物原因 (yes -> 反对; no -> 支持)
      known_reaction_pattern  : 是否为该药/同类已知反应 (yes/no/unknown)
      objective_evidence      : 是否有客观证据 (yes/no/unknown)
    """
    return {
        "previous_report": case.get("prior_history"),
        "acute_onset": case.get("onset_after_drug"),
        "dechallenge": case.get("dechallenge"),
        "rechallenge": case.get("rechallenge"),
        "alternative_cause": case.get("alternative_cause"),
        "known_reaction_pattern": case.get("known_reaction_pattern"),
        "objective_evidence": case.get("objective_evidence"),
    }


def from_faers_cases(cases):
    """Aggregate a list of FAERS case evidence dicts into one representative
    evidence dict using a conservative majority rule:

      supportive (+) count > contrary (-) count  -> +1
      contrary (-) count   > supportive (+) count -> -1
      otherwise (tie / all unknown)               -> 0 (unknown)

    This is a HEURISTIC summary of a case series, NOT a per-case verdict, and is
    explicitly labeled non-causal.
    """
    agg = {}
    for c in CRITERIA:
        pos = neg = 0
        for case in cases:
            ev = from_faers_case(case) if not isinstance(case, dict) else case
            sc = _encode(ev.get(c["key"]), c["polarity"])
            if sc > 0:
                pos += 1
            elif sc < 0:
                neg += 1
        if pos > neg:
            agg[c["key"]] = 1
        elif neg > pos:
            agg[c["key"]] = -1
        else:
            agg[c["key"]] = 0
    return agg


# ---------------------------------------------------------------------------
# CLI: 独立运行 / 被主流程调用。读取 JSON（evidence dict 或 case 列表）。
# ---------------------------------------------------------------------------
def _load_input(path):
    data = json.load(open(path, encoding="utf-8"))
    # 若为 case 列表（含 FAERS 病例字段），先聚合成 evidence
    if isinstance(data, list):
        return from_faers_cases(data)
    return data


def main():
    ap = argparse.ArgumentParser(
        description="Naranjo causality attribution (qualitative, non-causal).")
    ap.add_argument("--in", dest="infile",
                    help="JSON: a 7-key evidence dict OR a list of FAERS case dicts")
    ap.add_argument("--json-out", help="dump full assessment JSON")
    args = ap.parse_args()
    if not args.infile:
        ap.error("--in is required (path to evidence JSON)")
    evidence = _load_input(args.infile)
    res = naranjo_assessment(evidence)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", args.json_out)


if __name__ == "__main__":
    main()
