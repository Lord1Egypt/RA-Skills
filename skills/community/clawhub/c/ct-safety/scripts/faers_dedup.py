#!/usr/bin/env python3
"""faers_dedup.py - FAERS 病例级去重 / case-level de-duplication for FAERS.

问题 / The problem
------------------
FAERS 的原始个案报告里同一例病例会出现多次，这是公开文献反复强调的偏倚来源：

  1. **后续报告（follow-up）**：一例病例初次上报后补充信息，会以相同
     `safetyreportid`、递增 `safetyreportversion` 再次入库。
  2. **多方重复上报**：同一例可由生产企业、消费者、医务人员分别上报，
     `safetyreportid` 不同但描述同一个人同一次事件。

若不处理，个案清单会重复计数、夸大某个药—事件组合的报告量。

本模块做什么 / What this does
-----------------------------
两级、纯本地、零联网。输入是 `fetch_faers.fetch_case_reports()` 的输出
（或任何同结构的病例列表），输出去重结果 + 每条的 `dedup_reason`。

  L1 版本折叠（确定性，默认执行）
      同 `safetyreportid` 只保留 `safetyreportversion` 最大的一条。
      这一级是无争议的：旧版本被新版本取代，保留旧版必然重复计数。

  L2 疑似重复探测（启发式，默认只标记不删除）
      对 (性别, 归一年龄, 国家, 反应 PT 集合) 构造指纹。完全一致判 `exact`；
      人口学一致且 PT 集合 Jaccard ≥ 阈值（默认 0.8）判 `probable`。
      **默认只打标记，不删除** —— 药物警戒场景下静默丢弃病例是危险的，
      是否剔除应由分析者显式决定（`--drop-suspected`）。

刻意保留的局限 / Deliberate limitation
--------------------------------------
ct-safety 的 PRR / ROR / IC / EBGM 计数来自 openFDA 的 `count` 聚合端点，
那是服务端聚合的结果，**本地拿不到构成它的个案，因此无法对不成比例
分析的 2x2 表做病例级去重**。本模块只作用于 `fetch_case_reports` 抓回的
个案清单，用途是可追溯性与重复提示。任何基于本模块判定"信号被高估"
的结论都必须说明这一边界 —— 不要把个案层的去重率外推到聚合计数上。

隐私 / Privacy: FAERS 为公开去标识数据；本模块不联网、不写入任何患者标识。

用法 / Usage
-----------
    python faers_dedup.py --input cases.json --output deduped.json
    python faers_dedup.py --input cases.json --drop-suspected --jaccard 0.9

CLI 也可直接读 `fetch_case_reports` 写出的 `{"cases": [...]}` 包裹结构。
"""

import argparse
import json
import sys
from collections import defaultdict

# FAERS patientonsetageunit codes (openFDA):
# 800=Decade 801=Year 802=Month 803=Week 804=Day 805=Hour
_AGE_UNIT_TO_YEARS = {
    "800": 10.0,
    "801": 1.0,
    "802": 1.0 / 12.0,
    "803": 1.0 / 52.0,
    "804": 1.0 / 365.0,
    "805": 1.0 / 8760.0,
}


def normalize_age(age, unit):
    """Return age in whole years, or None when unusable.

    Ages are bucketed to integer years on purpose: a case re-reported as
    "45 years" vs "540 months" must collapse to the same fingerprint.
    """
    if age in (None, "", "null"):
        return None
    try:
        val = float(age)
    except (TypeError, ValueError):
        return None
    factor = _AGE_UNIT_TO_YEARS.get(str(unit).strip() if unit is not None else "801")
    if factor is None:
        factor = 1.0
    years = val * factor
    if years < 0 or years > 130:  # implausible -> treat as unknown
        return None
    return int(round(years))


def _version_int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return -1


def _pt_set(case):
    return frozenset(
        str(p).strip().lower()
        for p in (case.get("reaction_pt") or [])
        if p not in (None, "")
    )


def _country(case):
    c = case.get("occurcountry") or case.get("reportercountry") or ""
    return str(c).strip().upper() or None


def _sex(case):
    s = case.get("patientsex")
    if s in (None, ""):
        return None
    return str(s).strip()


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def collapse_versions(cases):
    """L1: keep only the highest safetyreportversion per safetyreportid.

    Cases without a safetyreportid cannot be version-collapsed and pass through
    untouched (they still go through L2).
    """
    best = {}
    passthrough = []
    dropped = []
    for c in cases:
        sid = c.get("safetyreportid")
        if sid in (None, ""):
            passthrough.append(c)
            continue
        sid = str(sid).strip()
        ver = _version_int(c.get("safetyreportversion"))
        if sid not in best:
            best[sid] = (ver, c)
        else:
            prev_ver, prev_c = best[sid]
            if ver > prev_ver:
                best[sid] = (ver, c)
                dropped.append((prev_c, sid, prev_ver, ver))
            else:
                dropped.append((c, sid, ver, prev_ver))

    kept = []
    for sid, (ver, c) in best.items():
        out = dict(c)
        superseded = [d for d in dropped if d[1] == sid]
        if superseded:
            out["dedup_reason"] = (
                "L1_version_collapse: kept version %s, superseded %d earlier "
                "version(s) of report %s" % (ver, len(superseded), sid)
            )
            out["dedup_level"] = "L1_version_collapse"
        kept.append(out)
    kept.extend(dict(c) for c in passthrough)
    return kept, dropped


def flag_suspected_duplicates(cases, jaccard_threshold=0.8):
    """L2: rule-based suspected-duplicate detection.

    Fingerprint = (sex, age-in-years, country, reaction-PT set).
    Identical fingerprint -> `exact`. Same demographics with PT-set Jaccard
    above the threshold -> `probable`.

    Returns (annotated_cases, clusters) where clusters maps a cluster id to the
    list of member indices. Nothing is removed here.
    """
    out = [dict(c) for c in cases]
    n = len(out)

    # --- exact fingerprint buckets ---
    exact_buckets = defaultdict(list)
    for i, c in enumerate(out):
        fp = (_sex(c), normalize_age(c.get("patientonsetage"),
                                     c.get("patientonsetageunit")),
              _country(c), _pt_set(c))
        # A fingerprint with no usable demographics AND no PTs carries no
        # evidence -- never cluster on emptiness.
        if fp[0] is None and fp[1] is None and fp[2] is None and not fp[3]:
            continue
        exact_buckets[fp].append(i)

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    evidence = defaultdict(list)
    for fp, members in exact_buckets.items():
        if len(members) < 2:
            continue
        for k in range(1, len(members)):
            union(members[0], members[k])
        for i in members:
            others = [out[j].get("safetyreportid") for j in members if j != i]
            evidence[i].append(
                ("exact", "identical sex/age/country/reaction-PT set; "
                          "other report id(s): %s" % ", ".join(str(o) for o in others[:3])))

    # --- probable: same demographics, high PT overlap ---
    demo_buckets = defaultdict(list)
    for i, c in enumerate(out):
        sex = _sex(c)
        age = normalize_age(c.get("patientonsetage"), c.get("patientonsetageunit"))
        ctry = _country(c)
        if sex is None or age is None or ctry is None:
            continue  # too little demographic evidence to risk a match
        demo_buckets[(sex, age, ctry)].append(i)

    for _key, members in demo_buckets.items():
        if len(members) < 2:
            continue
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                i, j = members[a], members[b]
                if find(i) == find(j):
                    continue
                sim = _jaccard(_pt_set(out[i]), _pt_set(out[j]))
                if sim >= jaccard_threshold:
                    union(i, j)
                    msg = ("same sex/age/country, reaction-PT Jaccard=%.2f "
                           ">= %.2f" % (sim, jaccard_threshold))
                    evidence[i].append(("probable", msg + " vs report %s"
                                        % out[j].get("safetyreportid")))
                    evidence[j].append(("probable", msg + " vs report %s"
                                        % out[i].get("safetyreportid")))

    # --- assign cluster ids and annotate ---
    clusters = defaultdict(list)
    for i in range(n):
        clusters[find(i)].append(i)

    for root, members in clusters.items():
        if len(members) < 2:
            continue
        cid = "D%04d" % root
        for i in members:
            ev = evidence.get(i) or []
            confidence = "exact" if any(t == "exact" for t, _ in ev) else "probable"
            out[i]["suspected_duplicate_cluster"] = cid
            out[i]["suspected_duplicate_confidence"] = confidence
            prior = out[i].get("dedup_reason")
            reason = "L2_suspected_duplicate (%s): %s" % (
                confidence,
                "; ".join(m for _t, m in ev[:2]) if ev
                else "linked transitively within cluster %s" % cid)
            out[i]["dedup_reason"] = (prior + " | " + reason) if prior else reason
            out[i]["dedup_level"] = ("L1_version_collapse+L2_suspected_duplicate"
                                     if prior else "L2_suspected_duplicate")

    real_clusters = {k: v for k, v in clusters.items() if len(v) > 1}
    return out, real_clusters


def dedup_cases(cases, jaccard_threshold=0.8, drop_suspected=False):
    """Run L1 + L2. Returns (cases, summary)."""
    raw_n = len(cases)
    kept, dropped_versions = collapse_versions(cases)
    after_l1 = len(kept)
    annotated, clusters = flag_suspected_duplicates(
        kept, jaccard_threshold=jaccard_threshold)

    n_flagged = sum(1 for c in annotated if c.get("suspected_duplicate_cluster"))
    n_exact = sum(1 for c in annotated
                  if c.get("suspected_duplicate_confidence") == "exact")
    n_probable = n_flagged - n_exact

    final = annotated
    n_dropped_l2 = 0
    if drop_suspected and clusters:
        # keep one representative per cluster: the highest version, then the
        # richest record (most reaction PTs) -- deterministic tie-breaking.
        drop_idx = set()
        for _root, members in clusters.items():
            rep = max(members, key=lambda i: (
                _version_int(annotated[i].get("safetyreportversion")),
                len(_pt_set(annotated[i])),
                str(annotated[i].get("safetyreportid") or ""),
            ))
            for i in members:
                if i != rep:
                    drop_idx.add(i)
        final = [c for i, c in enumerate(annotated) if i not in drop_idx]
        n_dropped_l2 = len(drop_idx)

    for c in final:
        c.setdefault("dedup_reason", "unique: no duplicate evidence found")
        c.setdefault("dedup_level", "none")

    summary = {
        "raw_cases": raw_n,
        "after_l1_version_collapse": after_l1,
        "l1_versions_superseded": len(dropped_versions),
        "l2_suspected_duplicate_cases": n_flagged,
        "l2_clusters": len(clusters),
        "l2_exact": n_exact,
        "l2_probable": n_probable,
        "l2_dropped": n_dropped_l2,
        "final_cases": len(final),
        "jaccard_threshold": jaccard_threshold,
        "drop_suspected": bool(drop_suspected),
        "limitation": (
            "病例级去重仅作用于个案清单；PRR/ROR/IC/EBGM 的计数来自 openFDA "
            "聚合端点，无法在本地做病例级去重，故不成比例分析结果未被此处修正。"
            " / Case-level de-duplication applies to the case listing only; "
            "PRR/ROR/IC/EBGM counts come from openFDA aggregate endpoints and "
            "cannot be de-duplicated locally, so disproportionality results are "
            "NOT corrected by this module."
        ),
    }
    return final, summary


def format_summary(summary, lang="zh"):
    """Human-readable summary block for reports."""
    s = summary
    if lang == "zh":
        L = ["### FAERS 病例级去重 / case-level de-duplication",
             "- 原始个案 / raw cases: %d" % s["raw_cases"],
             "- L1 版本折叠后 / after version collapse: %d（取代旧版本 %d 条）"
             % (s["after_l1_version_collapse"], s["l1_versions_superseded"]),
             "- L2 疑似重复 / suspected duplicates: %d 例，聚为 %d 簇"
             "（确定重复 %d，疑似 %d）"
             % (s["l2_suspected_duplicate_cases"], s["l2_clusters"],
                s["l2_exact"], s["l2_probable"])]
        if s["drop_suspected"]:
            L.append("- 已剔除疑似重复 / dropped: %d（每簇保留 1 条代表）" % s["l2_dropped"])
        else:
            L.append("- 疑似重复仅标记未剔除（药物警戒场景下不静默丢弃病例；"
                     "需剔除请用 --drop-suspected）")
        L.append("- 最终个案 / final cases: %d" % s["final_cases"])
        L.append("- ⚠️ 局限：%s" % s["limitation"].split(" / ")[0])
    else:
        L = ["### FAERS case-level de-duplication",
             "- raw cases: %d" % s["raw_cases"],
             "- after L1 version collapse: %d (%d earlier versions superseded)"
             % (s["after_l1_version_collapse"], s["l1_versions_superseded"]),
             "- L2 suspected duplicates: %d cases in %d clusters "
             "(exact %d, probable %d)"
             % (s["l2_suspected_duplicate_cases"], s["l2_clusters"],
                s["l2_exact"], s["l2_probable"])]
        if s["drop_suspected"]:
            L.append("- dropped: %d (one representative kept per cluster)" % s["l2_dropped"])
        else:
            L.append("- suspected duplicates are FLAGGED, not removed "
                     "(use --drop-suspected to filter)")
        L.append("- final cases: %d" % s["final_cases"])
        L.append("- WARNING: %s" % s["limitation"].split(" / ")[-1])
    return "\n".join(L)


def _load_cases(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        if isinstance(data.get("cases"), list):
            return data["cases"], data
        for key in ("results", "records", "items"):
            if isinstance(data.get(key), list):
                return data[key], data
        raise SystemExit("input JSON dict has no 'cases'/'results'/'records' list")
    if isinstance(data, list):
        return data, None
    raise SystemExit("unsupported input JSON structure")


def main():
    ap = argparse.ArgumentParser(
        description="FAERS case-level de-duplication (pure local, no network).")
    ap.add_argument("--input", required=True,
                    help="JSON from fetch_faers.fetch_case_reports (or a bare case list)")
    ap.add_argument("--output", help="write de-duplicated JSON here")
    ap.add_argument("--jaccard", type=float, default=0.8,
                    help="reaction-PT Jaccard threshold for 'probable' duplicates (default 0.8)")
    ap.add_argument("--drop-suspected", action="store_true",
                    help="actually remove L2 suspected duplicates (default: flag only)")
    ap.add_argument("--lang", choices=["zh", "en"], default="zh")
    args = ap.parse_args()

    cases, wrapper = _load_cases(args.input)
    final, summary = dedup_cases(cases, jaccard_threshold=args.jaccard,
                                 drop_suspected=args.drop_suspected)
    print(format_summary(summary, lang=args.lang))

    if args.output:
        payload = dict(wrapper) if isinstance(wrapper, dict) else {}
        payload["cases"] = final
        payload["dedup_summary"] = summary
        payload["n_fetched"] = len(final)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print("\n[OK] wrote %s" % args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
