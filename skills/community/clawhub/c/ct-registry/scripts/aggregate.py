#!/usr/bin/env python3
"""aggregate.py - Aggregate normalized trials + de-duplication / 聚合分析 + 跨库去重.

De-duplication strategy (ct-registry 分源直连 + 自建桥接, 2026-07-24)
--------------------------------------------------------------
WHO ICTRP 自 2026-07-27 起重新成为数据源（Tier-2 外部服务，source="who"），其价值是
一次镜像 14+ 一级注册库（jRCT / DRKS / ANZCTR / ISRCTN / CTRI / ...）。本聚合层用自建
桥接逻辑在 ICTRP 记录与其他源之间做跨库去重与关联：CT.gov / CDE / ChiCTR / EU CTR /
ISRCTN / DRKS / ICTRP 各自拉回原始记录，聚合层做跨源去重，否则跨库计数翻倍、字段冲突。
三级去重键（优先级从高到低）：

  1. 注册号归一化：NCT######## / EUCTR... / ChiCTR... / ISRCTN... / JPRN... / DRKS...
     等互相引用的注册号直接关联；同一记录 raw 文本里命中的其他注册号作为 secondary_ids 桥接。
  2. 模糊匹配：(归一化标题 + 申办方 + 入组年份 ±1 + 首个干预) 相似度聚类，识别"隐藏重复"
     （如印度试验仅登 CTRI 但标题与 CT.gov 一致）。
  3. 主源选择：同组优先以 CT.gov 为 primary_source（字段最完整、更新最频繁），否则取字段最全者。

架构落点：归一化层保留各库原始记录；聚合层追加 dedup_group_id / primary_source /
registry_id_norm / secondary_ids / dedup_reason / dedup_tier 六个字段，并产出 dedup_summary。

P1-C: FDA 多模态数据整合（drug_approvals/shortages/recalls）
P1-E: MinHash 预聚类替代 O(n²) 模糊匹配，降为近似 O(n log n)
P1-F: 去重可审计化。每条记录输出 dedup_reason（合并证据）+ dedup_tier
      （tier1_id_bridge / tier2_fuzzy / transitive / none），dedup_summary 增加
      merge_edges 与 dedup_tier_breakdown。动机：非英文试验（CDE/ChiCTR）靠自由文本
      注册号桥接，误并（false positive）与正确合并在只有 group_id 时无法区分；
      tier2_fuzzy 仅凭"标题+单一佐证"即合并，风险最高，必须留证据可回溯。
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    # R10: single source of truth for phase canonicalisation (see normalize.py).
    from normalize import canon_phase, sponsor_key, canon_status
except Exception:  # pragma: no cover - normalize.py always ships alongside
    def canon_phase(v):
        return v

    def sponsor_key(v):
        return (str(v).strip().lower() or None) if v else None

    def canon_status(v):
        return v

# 已知注册号模式（用于归一化与跨库桥接）
# NOTE: fixed-length id patterns use a negative lookahead `(?!\d)` so a longer
# digit run is NOT silently truncated into a shared (colliding) id. e.g. an
# 11-digit NCT-like string "NCT10000000000" would otherwise extract as the same
# 8-digit "NCT10000000" for every record and bridge them all in Tier 1.
ID_PATTERNS = [
    r"NCT\d{8}(?!\d)",
    r"EUCTR[\d-]+",
    # EudraCT numbers are routinely cited as "EudraCT 2023-000123-45" in free
    # text; captured here and aliased onto the EUCTR prefix below so they bridge
    # to EU CTR records (see _ID_ALIAS).
    r"EudraCT[\s:-]*\d{4}-\d{6}-\d{2}",
    # ChiCTR ids come in TWO real shapes and the old `ChiCTR\d{8}` matched
    # NEITHER, so Tier-1 bridging never fired for real ChiCTR data:
    #   * modern:  ChiCTR2400079823   (prefix + 10 digits)
    #   * legacy:  ChiCTR-IOR-17010085 / ChiCTR-TRC-14004108 (dashed, 3-letter
    #     study-type segment + 8 digits)
    r"ChiCTR(?:-[A-Za-z]{2,4})?-?\d{8,12}(?!\d)",
    r"ISRCTN\d{8}(?!\d)",
    r"JPRN[\w-]+",
    r"DRKS\d+",
    r"ACTRN\d{14}(?!\d)",
    r"UTN\d+",
    r"CTRI/[\w/]+",
    # China CDE registration number (CTR + 4-digit year + 4-digit serial), e.g.
    # CTR20240001. Absent before v0.3.61, so a CDE id cited inside another
    # registry's free text never bridged back to the CDE record. Must stay
    # AFTER CTRI/ and ACTRN so those longer prefixes win at the same offset.
    r"CTR\d{8}(?!\d)",
    r"TCTR\d+",
    r"PACTR\d+",
    r"RPCEC\d+",
    r"REPEC\d+",
    r"SLCTR\d+",
    r"LBCTR\d+",
    r"IRCT\d+",
    r"RBR\d+",
    r"CURTR\d+",
    r"KCT\d+",
]
_ID_RE = re.compile("|".join(ID_PATTERNS), re.IGNORECASE)


def norm_id(raw):
    """Normalize a registry id for cross-source matching."""
    if not raw:
        return None
    s = re.sub(r"[\s\-]", "", str(raw)).upper()
    # strip a common wrapping like "NCT12345678" stays; keep alphanumerics
    return s or None


# Prefix aliases: different names for the SAME registry must normalize to one
# form, otherwise a free-text citation never bridges to the record itself.
_ID_ALIAS = (("EUDRACT", "EUCTR"),)


def extract_ids(text):
    """Extract known registry-id patterns from free text (for bridging)."""
    if not text:
        return []
    out = []
    for m in _ID_RE.finditer(text):
        tok = m.group(0).upper().replace(" ", "").replace(":", "")
        for src, dst in _ID_ALIAS:
            if tok.startswith(src):
                tok = dst + tok[len(src):].lstrip("-")
                break
        out.append(tok)
    return out


def _norm_text(s):
    if not s:
        return ""
    # PRESERVE CJK (U+4E00–U+9FFF): stripping it collapsed Chinese titles into
    # their bare ASCII drug codes (e.g. "评估AK112…的II期研究" -> "ak112"), which
    # made unrelated CDE trials sharing a drug code look identical and get
    # OVER-MERGED in Tier-2 fuzzy dedup (real-run 2026-08-03: 278/1347 records,
    # 20.6%, silently lost). Keeping CJK preserves each title's distinguishing text.
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", str(s).lower())


def _title_key(s):
    """First ~6 significant tokens of a normalized title (fuzzy cluster key)."""
    toks = _norm_text(s).split()[:6]
    return " ".join(toks)


# A title key shorter than this is too generic to trust substring matching: a bare
# ASCII drug code (e.g. "ak112"=5, "tqb2450"=7) would otherwise swallow every trial
# that merely mentions it. Exact equality is always trusted regardless of length.
_MIN_TITLE_CHARS = 8


def _title_match(tk_i, tk_j):
    """Tier-2 fuzzy title match: do these two normalized titles denote the same trial?

    - Exact equality always matches (true duplicates, incl. short bare titles).
    - Substring containment is allowed ONLY when BOTH keys are long enough, so a
      short drug code can never over-merge distinct trials that share it. With CJK
      preserved, Chinese titles stay distinctive, so unrelated Chinese CDE trials no
      longer collapse onto one drug code either.
    """
    if not (tk_i and tk_j):
        return False
    if tk_i == tk_j:
        return True
    if len(tk_i) >= _MIN_TITLE_CHARS and len(tk_j) >= _MIN_TITLE_CHARS:
        return tk_i in tk_j or tk_j in tk_i
    return False


def _year(d):
    # Robust year extraction: handles YYYY-MM-DD (CT.gov/CDE), DD/MM/YYYY
    # (WHO ICTRP detail), YYYY/MM/DD, and bare YYYY. Uses a regex so the year
    # can appear at ANY position (e.g. WHO detail "30/12/2024" -> 2024), not
    # only at the front.
    if isinstance(d, str):
        m = re.search(r"(?:19|20)\d{2}", d)
        if m:
            return m.group(0)
    return None


def _record_ids(rec):
    """All ids associated with a record: own registry_id + ids found in text."""
    ids = set()
    rid = norm_id(rec.get("registry_id"))
    if rid:
        ids.add(rid)
    blob = " ".join(str(rec.get(k) or "") for k in ("title", "raw", "url"))
    for x in extract_ids(blob):
        ids.add(norm_id(x))
    return ids


def _field_count(rec):
    return sum(1 for k in ("title", "status", "phase", "conditions",
                           "interventions", "sponsor", "start_date",
                           "enrollment", "drug") if rec.get(k))


# ── P1-E: MinHash pre-clustering ────────────────────────────────────────
# Replace the O(n²) Tier-2 fuzzy match with an approximate O(n log n) approach:
#   1. Compute a MinHash signature for each record's title_key (character n-grams).
#   2. Hash signatures into bands; records sharing a band go into the same candidate bucket.
#   3. Only compare pairs within the same bucket (dramatically fewer comparisons).
# This is a pure-Python implementation using hashlib — no third-party dependencies.
# The trade-off: a small false-negative rate (some true duplicates may be missed),
# controlled by (num_bands, rows_per_band) parameters.

def _ngrams(text, n=3):
    """Generate character n-grams from text (used for MinHash signatures)."""
    if not text:
        return []
    text = str(text).lower()
    # pad with boundary chars for short texts
    padded = f"^{text}$$"
    return [padded[i:i+n] for i in range(len(padded) - n + 1)]


def _minhash_signature(text, num_hashes=64, ngram_size=3):
    """Compute a MinHash signature for a text string.

    Uses multiple hash functions simulated via salted SHA-256.
    Returns a tuple of integers (the signature).
    """
    grams = set(_ngrams(text, ngram_size))
    if not grams:
        return tuple([0] * num_hashes)
    signature = []
    for seed in range(num_hashes):
        min_hash = None
        for g in grams:
            h = hashlib.sha256(f"{seed}:{g}".encode('utf-8')).hexdigest()
            val = int(h[:8], 16)
            if min_hash is None or val < min_hash:
                min_hash = val
        signature.append(min_hash)
    return tuple(signature)


def _lsh_buckets(signature, num_bands=8, rows_per_band=None):
    """Hash a MinHash signature into LSH band buckets.

    Returns a list of (band_idx, bucket_hash) tuples. Two records sharing
    the same (band_idx, bucket_hash) are candidate duplicates.
    """
    if rows_per_band is None:
        rows_per_band = max(1, len(signature) // num_bands)
    buckets = []
    for band_idx in range(num_bands):
        start = band_idx * rows_per_band
        end = start + rows_per_band
        if end > len(signature):
            break
        band_slice = signature[start:end]
        bucket_hash = hashlib.sha256(
            f"{band_idx}:{band_slice}".encode('utf-8')).hexdigest()[:12]
        buckets.append((band_idx, bucket_hash))
    return buckets


def _minhash_candidate_pairs(records, sig_list, num_bands=8, num_hashes=64):
    """Find candidate duplicate pairs using LSH pre-clustering.

    Returns a set of (i, j) index pairs (i < j) that share at least one LSH bucket.
    This replaces the O(n²) all-pairs comparison with near-linear candidate generation.
    """
    # Build LSH index: band -> set of record indices
    band_index = defaultdict(set)
    signatures = []
    for i, sig_text in enumerate(sig_list):
        sig = _minhash_signature(sig_text, num_hashes=num_hashes)
        signatures.append(sig)
        for bucket_key in _lsh_buckets(sig, num_bands=num_bands):
            band_index[bucket_key].add(i)
    # Generate candidate pairs from bands
    candidates = set()
    for bucket_members in band_index.values():
        if len(bucket_members) < 2:
            continue
        members = sorted(bucket_members)
        for a in range(len(members)):
            for b in range(a + 1, len(members)):
                candidates.add((members[a], members[b]))
    return candidates, signatures


def dedup(records):
    """Group records into de-duplication clusters; tag primary_source + group id.

    Returns (tagged_records, summary).

    P1-E: Tier-2 fuzzy match uses MinHash + LSH pre-clustering for near O(n log n) performance.
    """
    n = len(records)
    parent = list(range(n))

    # P1-F: per-merge audit trail. Every union() that actually collapses two
    # clusters records WHY, so each output record can carry a human-readable
    # dedup_reason instead of an opaque group id. Motivation: non-English
    # trials (CDE/ChiCTR) bridge through free-text registry numbers, and a
    # silent over-merge (false positive) is indistinguishable from a correct
    # merge without the evidence that triggered it.
    merge_edges = []  # (i, j, tier, evidence)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    # --- Tier 1: registration-number normalization + secondary-id bridging ---
    id_to_idx = {}
    for i, rec in enumerate(records):
        for rid in _record_ids(rec):
            if rid in id_to_idx:
                other = id_to_idx[rid]
                if other != i and find(i) != find(other):
                    merge_edges.append((i, other, "tier1_id_bridge",
                                        f"shared registry id {rid}"))
                union(i, other)
            else:
                id_to_idx[rid] = i

    # --- Tier 2: fuzzy match with MinHash + LSH pre-clustering (P1-E) ---
    sig = []
    sig_text = []  # raw title_key for MinHash
    for rec in records:
        tk = _title_key(rec.get("title"))
        sp = _norm_text(rec.get("sponsor"))
        yr = _year(rec.get("start_date"))
        iv = _norm_text((rec.get("interventions") or [None])[0] if isinstance(
            rec.get("interventions"), list) else rec.get("interventions"))
        sig.append((tk, sp, yr, iv))
        sig_text.append(tk)

    # Use LSH to find candidate pairs (near-linear)
    candidates, _ = _minhash_candidate_pairs(records, sig_text, num_bands=8, num_hashes=64)

    # Verify candidates with the original fuzzy match logic
    for i, j in candidates:
        if not sig[i][0] or not sig[j][0]:
            continue
        if find(i) == find(j):
            continue
        tk_i, sp_i, yr_i, iv_i = sig[i]
        tk_j, sp_j, yr_j, iv_j = sig[j]
        title_ok = _title_match(tk_i, tk_j)
        if not title_ok:
            continue
        sponsor_ok = (sp_i and sp_i == sp_j)
        year_ok = (yr_i and yr_j and yr_i == yr_j)
        iv_ok = (iv_i and iv_i == iv_j)
        # title must match; sponsor/year/intervention at least one corroborates
        if sponsor_ok or year_ok or iv_ok:
            corroborators = []
            if sponsor_ok:
                corroborators.append("sponsor")
            if year_ok:
                corroborators.append(f"start_year={yr_i}")
            if iv_ok:
                corroborators.append("intervention")
            merge_edges.append((i, j, "tier2_fuzzy",
                                "title match + " + "/".join(corroborators)))
            union(i, j)

    # --- assign group ids + collect members ---
    groups = {}
    for i in range(n):
        g = find(i)
        groups.setdefault(g, []).append(i)

    # --- P1-F: per-record merge evidence, keyed by record index ---
    def _label(idx):
        src = records[idx].get("source") or "?"
        rid = norm_id(records[idx].get("registry_id")) or "no-id"
        return f"{src}:{rid}"

    edge_evidence = defaultdict(list)
    for a, b, tier, ev in merge_edges:
        edge_evidence[a].append((tier, ev, b))
        edge_evidence[b].append((tier, ev, a))

    # --- Tier 3: choose primary_source per group (CT.gov preferred) ---
    tagged = [dict(r) for r in records]
    for gid, members in groups.items():
        primary = None
        for i in members:
            if tagged[i].get("source") == "CTGOV":
                primary = i
                break
        if primary is None:
            primary = max(members, key=lambda i: _field_count(tagged[i]))
        for i in members:
            tagged[i]["dedup_group_id"] = f"G{gid:04d}"
            tagged[i]["primary_source"] = (i == primary)
            tagged[i]["registry_id_norm"] = norm_id(tagged[i].get("registry_id"))
            # secondary ids = all ids in group except own
            grp_ids = set()
            for j in members:
                grp_ids |= _record_ids(tagged[j])
            own = tagged[i].get("registry_id_norm")
            tagged[i]["secondary_ids"] = sorted(grp_ids - ({own} if own else set()))

            # P1-F: explain this record's membership. Direct evidence wins;
            # union-find is a transitive closure, so a record can legitimately
            # land in a cluster without a direct edge (A-B, B-C => A,C linked).
            ev = edge_evidence.get(i) or []
            if ev:
                tiers = sorted({t for t, _, _ in ev})
                parts = [f"{t} ({e}) <-> {_label(o)}" for t, e, o in ev[:3]]
                if len(ev) > 3:
                    parts.append(f"+{len(ev) - 3} more")
                tagged[i]["dedup_reason"] = "; ".join(parts)
                tagged[i]["dedup_tier"] = "+".join(tiers)
            elif len(members) > 1:
                peers = ", ".join(_label(j) for j in members if j != i)
                if len(peers) > 160:
                    peers = peers[:157] + "..."
                tagged[i]["dedup_reason"] = f"transitive: joined cluster via {peers}"
                tagged[i]["dedup_tier"] = "transitive"
            else:
                tagged[i]["dedup_reason"] = "singleton: no cross-registry match"
                tagged[i]["dedup_tier"] = "none"

    # --- summary ---
    cross_source = sum(1 for m in groups.values()
                       if len({tagged[i].get("source") for i in m}) > 1)
    # P1-F: tier breakdown makes over-merge / under-merge auditable at a glance.
    tier_breakdown = Counter(r.get("dedup_tier") or "none" for r in tagged)
    summary = {
        "raw_total": n,
        "groups": len(groups),
        "deduped_total": len(groups),
        "removed": n - len(groups),
        "cross_source_groups": cross_source,
        "minhash_candidates": len(candidates),
        "minhash_bands": 8,
        "merge_edges": len(merge_edges),
        "dedup_tier_breakdown": dict(sorted(tier_breakdown.items())),
    }
    return tagged, summary


# ── P1-C: FDA event integration ──────────────────────────────────────────
# Load local FDA event cache (OpenFDA public data exported to JSON).
# Each event: {"event_type": "drug_approval"|"shortage"|"recall", "drug": "...", "date": "...", "detail": "..."}
# The cache file is maintained externally (quarterly update script) and NOT fetched at runtime.

def _load_fda_events(cache_path=None):
    """Load FDA events from a local JSON cache file.

    Expected format: {"drug_approvals": [...], "shortages": [...], "recalls": [...]}
    Each item: {"drug": "...", "date": "YYYY-MM-DD", "detail": "..."}

    Returns a dict keyed by lowercase drug name for fast lookup.
    """
    if cache_path is None:
        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "references", "fda_events_cache.json")
    if not os.path.exists(cache_path):
        return {}
    try:
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}
    events_by_drug = defaultdict(list)
    for event_type in ("drug_approvals", "shortages", "recalls"):
        for item in data.get(event_type, []):
            drug = (item.get("drug") or "").strip().lower()
            if drug:
                events_by_drug[drug].append({
                    "event_type": event_type.rstrip('s'),  # drug_approval / shortage / recall
                    "date": item.get("date"),
                    "detail": item.get("detail", ""),
                })
    return dict(events_by_drug)


def _match_fda_events(records, fda_events):
    """Match FDA events to trial records by drug name.

    For each primary record, look up its drug field in the FDA events cache.
    Returns a summary dict with counts and matched events per drug.
    """
    if not fda_events:
        return {"available": False, "matched_drugs": 0, "total_events": 0, "events_by_type": {}}
    matched = {}
    events_by_type = Counter()
    for rec in records:
        drug = (rec.get("drug") or "").strip().lower()
        if not drug:
            continue
        # exact match + partial match (e.g. "pembrolizumab" matches "keytruda (pembrolizumab)")
        events = fda_events.get(drug, [])
        if not events:
            # try partial: any FDA drug that is a substring of trial drug or vice versa
            for fda_drug, evts in fda_events.items():
                if fda_drug in drug or drug in fda_drug:
                    events = evts
                    break
        if events:
            matched[drug] = events
            for e in events:
                events_by_type[e["event_type"]] += 1
    return {
        "available": True,
        "matched_drugs": len(matched),
        "total_events": sum(len(v) for v in matched.values()),
        "events_by_type": dict(events_by_type),
        "matched": matched,
    }


def aggregate(records, fda_cache_path=None):
    # de-duplicate first; distributions computed on PRIMARY records only
    tagged, dsum = dedup(records)
    primaries = [r for r in tagged if r.get("primary_source")]
    # R10: canonicalise defensively — records may arrive pre-normalized from an
    # older run (or hand-assembled), in which case normalize.py never ran.
    phase = Counter(canon_phase(r.get("phase")) or "Unknown" for r in primaries)
    status = Counter(canon_status(r.get("status")) or "Unknown" for r in primaries)
    # R5: group sponsors by canonical key so one company written five ways is
    # ONE entry in the ranking. The label shown is the most frequent raw
    # spelling in the group (ties -> longest, i.e. the most informative form).
    _sp_groups = {}
    for r in primaries:
        raw = r.get("sponsor") or "Unknown"
        k = r.get("sponsor_key") or sponsor_key(raw) or str(raw).strip().lower()
        g = _sp_groups.setdefault(k, {"n": 0, "labels": Counter()})
        g["n"] += 1
        g["labels"][str(raw).strip()] += 1
    sponsor = Counter()
    for k, g in _sp_groups.items():
        label = max(g["labels"].items(), key=lambda kv: (kv[1], len(kv[0])))[0]
        sponsor[label] = g["n"]
    years = Counter()
    for r in primaries:
        d = r.get("start_date") or ""
        y = _year(d)
        if y:
            years[y] += 1
    comp = {}
    for r in primaries:
        for cond in (r.get("conditions") or []):
            comp.setdefault(cond, set()).add(
                r.get("sponsor_key") or sponsor_key(r.get("sponsor"))
                or r.get("sponsor"))
    competitor_map = {c: len(s) for c, s in comp.items()}

    # P1-C: FDA event integration (local cache only, no network)
    fda_events = _load_fda_events(fda_cache_path)
    fda_summary = _match_fda_events(primaries, fda_events)

    return {
        "total": len(primaries),
        "phase_dist": dict(phase.most_common()),
        "status_dist": dict(status.most_common()),
        "top_sponsors": dict(sponsor.most_common(10)),
        "timeline": dict(sorted(years.items())),
        "competitor_map": dict(sorted(competitor_map.items(), key=lambda x: -x[1])[:20]),
        "fda_events": fda_summary,
        "dedup_summary": dsum,
        "records": primaries,
        "records_all": tagged,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", default="agg.json")
    ap.add_argument("--fda-cache", dest="fda_cache", default=None,
                    help="path to local FDA events cache JSON (default: ../references/fda_events_cache.json)")
    args = ap.parse_args()
    with open(args.inp, encoding="utf-8") as f:
        records = json.load(f)
    agg = aggregate(records, fda_cache_path=args.fda_cache)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(agg, f, ensure_ascii=False, indent=2)
    d = agg["dedup_summary"]
    print(f"[aggregate] raw={d['raw_total']} groups={d['groups']} "
          f"deduped={d['deduped_total']} removed={d['removed']} "
          f"cross_source={d['cross_source_groups']} "
          f"minhash_candidates={d.get('minhash_candidates', 'n/a')} -> {args.out}")
    fda = agg.get("fda_events", {})
    if fda.get("available"):
        print(f"[aggregate] FDA events: {fda['matched_drugs']} drugs matched, "
              f"{fda['total_events']} total events ({fda['events_by_type']})")


if __name__ == "__main__":
    main()
