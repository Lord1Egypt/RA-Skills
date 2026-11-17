#!/usr/bin/env python3
"""track_diff.py - Local-only trial status change / snapshot diff for ct-registry.

Pure-local: reads two ``normalized.json`` snapshots (each a list of records with
``registry_id`` + canonical ``status``), diffs by NCT / registry_id set, and emits
a ``status_delta`` list. No network is touched.

``track`` writes the current normalized result to ``registry_snapshot.json`` so the
next run can diff against it.

Only the *status* field is compared. Fine wording drift that maps to the same
lifecycle bucket is surfaced as ``spelling_change`` rather than ``status_change``
so legitimate source-spelling churn does not create false-positive deltas.

Multi-field diff (P1-D): extends the original status-only comparison with
phase / sponsor / conditions dimensions. Each dimension is compared with its own
normalisation (canon_phase / sponsor_key / Jaccard) so cross-source wording drift
does not create false positives.
"""
import argparse
import json
import os
import shutil
import sys

# --- Status equivalence map (coarse lifecycle buckets) -------------------
# Used ONLY for diff comparison: synonymous canonical statuses that should NOT
# be reported as a "real" change. This is intentionally coarser than
# ``normalize.canon_status`` — its sole purpose is to suppress false-positive
# deltas from wording drift across registries.
#
# Grouping rationale (ct-registry P0-A):
#   * RECRUITING / ACTIVE_NOT_RECRUITING / ONGOING / NOT_YET_RECRUITING
#     all mean "the trial is alive / not closed"  -> bucket "ACTIVE".
#     (RECRUITING ≈ ACTIVE 一类: recruiting and active-not-recruiting are both
#      ongoing programmes; a wording flip between them is not a status change.)
#   * COMPLETED stands alone.
#   * TERMINATED / SUSPENDED / WITHDRAWN all mean "closed / no longer enrolling"
#     -> bucket "CLOSED".
#   * UNKNOWN stays its own bucket.
STATUS_EQUIV = {
    "NOT_YET_RECRUITING": "ACTIVE",
    "RECRUITING": "ACTIVE",
    "ACTIVE_NOT_RECRUITING": "ACTIVE",
    "ONGOING": "ACTIVE",
    "COMPLETED": "COMPLETED",
    "TERMINATED": "CLOSED",
    "SUSPENDED": "CLOSED",
    "WITHDRAWN": "CLOSED",
    "UNKNOWN": "UNKNOWN",
}


def _bucket(status):
    """Map a canonical status onto its coarse lifecycle bucket (uppercased)."""
    if status is None:
        return None
    return STATUS_EQUIV.get(str(status).upper(), str(status).upper())


def load_record_status(path):
    """Return ``{registry_id: {"status": canonical, ..., "title": ..., "phase_raw": ..., "sponsor_raw": ...}}``.

    Accepts a normalized.json that is either a bare list of records or an object
    carrying a ``records`` list (both shapes exist in this skill's pipelines).
    P1-D: extended to capture phase / sponsor / conditions for multi-field diff.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    recs = data if isinstance(data, list) else data.get("records", [])
    out = {}
    for r in recs:
        rid = r.get("registry_id")
        if not rid:
            continue
        st = r.get("status")
        out[str(rid)] = {
            "status": st,
            "status_raw": r.get("status_raw") or st,
            "title": r.get("title"),
            "phase": r.get("phase"),
            "phase_raw": r.get("phase_raw"),
            "sponsor": r.get("sponsor"),
            "sponsor_raw": r.get("sponsor_raw"),
            "conditions": r.get("conditions") or [],
        }
    return out


def _phase_bucket(phase_val):
    """Best-effort phase bucket: extract a sortable numeric tuple for comparison.

    Normalises common spellings so cross-source wording drift doesn't fire deltas.
    Returns a tuple of ints, e.g. (3,) for PHASE 3, (1, 2) for PHASE 1/PHASE 2.
    Unrecognisable values fall back to a string hash so genuine changes still surface.
    """
    if not phase_val:
        return None
    import re
    s = str(phase_val).strip()
    # roman / arabic numerals
    romans = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4}
    nums = []
    for tok in re.findall(r'[ivx]+|\d+', s.lower()):
        if tok in romans:
            nums.append(romans[tok])
        elif tok.isdigit():
            nums.append(int(tok))
    if nums:
        return tuple(sorted(set(nums)))
    return (hash(s) % 10000,)


def _sponsor_key(s):
    """Minimal sponsor normalisation: strip legal suffixes + lowercase."""
    if not s:
        return None
    import re
    s = str(s).strip().lower()
    # strip common legal suffixes
    s = re.sub(r'[\s,.\-_/&\'"]+', ' ', s)
    for suffix in ['co', 'ltd', 'limited', 'inc', 'incorporated', 'llc',
                   'plc', 'corp', 'corporation', 'gmbh', 'ag', 'sa', 'nv',
                   'bv', 'pty', 'kk', 'company', 'holdings', 'group',
                   '股份', '有限', '责任', '公司', '集团', '控股']:
        s = re.sub(r'(^|\s)' + suffix + r'(\s|$)', ' ', s)
    s = s.strip()
    return s or None


def _jaccard(a, b):
    """Jaccard similarity between two lists (treated as sets)."""
    sa, sb = set(a or []), set(b or [])
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def diff_snapshots(a_path, b_path):
    """Diff two normalized.json snapshots; return a status_delta report dict.

    P1-D: extends the original status-only comparison with phase / sponsor /
    conditions dimensions. Each dimension is compared with its own normalisation
    so cross-source wording drift does not create false positives.
    """
    a = load_record_status(a_path)
    b = load_record_status(b_path)
    ka, kb = set(a), set(b)
    added = sorted(kb - ka)
    removed = sorted(ka - kb)
    common = sorted(ka & kb)
    deltas = []
    for rid in added:
        deltas.append({
            "nct": rid, "old_status": None, "new_status": b[rid]["status"],
            "change_type": "added",
        })
    for rid in removed:
        deltas.append({
            "nct": rid, "old_status": a[rid]["status"], "new_status": None,
            "change_type": "removed",
        })
    for rid in common:
        os_ = a[rid]["status"]
        ns_ = b[rid]["status"]
        if os_ != ns_:
            if _bucket(os_) == _bucket(ns_):
                ct = "spelling_change"
            else:
                ct = "status_change"
            deltas.append({
                "nct": rid, "old_status": os_, "new_status": ns_,
                "change_type": ct,
                "old_bucket": _bucket(os_), "new_bucket": _bucket(ns_),
            })
        # --- P1-D: phase delta ---
        op = _phase_bucket(a[rid].get("phase"))
        np_ = _phase_bucket(b[rid].get("phase"))
        if op != np_:
            deltas.append({
                "nct": rid,
                "change_type": "phase_change",
                "old_phase": a[rid].get("phase_raw") or a[rid].get("phase"),
                "new_phase": b[rid].get("phase_raw") or b[rid].get("phase"),
                "old_phase_bucket": op,
                "new_phase_bucket": np_,
            })
        # --- P1-D: sponsor delta ---
        osp = _sponsor_key(a[rid].get("sponsor"))
        nsp = _sponsor_key(b[rid].get("sponsor"))
        if osp != nsp:
            deltas.append({
                "nct": rid,
                "change_type": "sponsor_change",
                "old_sponsor": a[rid].get("sponsor_raw") or a[rid].get("sponsor"),
                "new_sponsor": b[rid].get("sponsor_raw") or b[rid].get("sponsor"),
                "old_sponsor_key": osp,
                "new_sponsor_key": nsp,
            })
        # --- P1-D: conditions delta (Jaccard) ---
        oc = a[rid].get("conditions", [])
        nc = b[rid].get("conditions", [])
        j = _jaccard(oc, nc)
        if j < 1.0:
            deltas.append({
                "nct": rid,
                "change_type": "conditions_change",
                "old_conditions": oc,
                "new_conditions": nc,
                "jaccard_similarity": round(j, 3),
                "added_conditions": sorted(set(nc) - set(oc)),
                "removed_conditions": sorted(set(oc) - set(nc)),
            })
    return {
        "snapshot_a": a_path,
        "snapshot_b": b_path,
        "n_a": len(ka),
        "n_b": len(kb),
        "added": len(added),
        "removed": len(removed),
        "status_change": sum(1 for d in deltas if d["change_type"] == "status_change"),
        "spelling_change": sum(1 for d in deltas if d["change_type"] == "spelling_change"),
        "phase_change": sum(1 for d in deltas if d["change_type"] == "phase_change"),
        "sponsor_change": sum(1 for d in deltas if d["change_type"] == "sponsor_change"),
        "conditions_change": sum(1 for d in deltas if d["change_type"] == "conditions_change"),
        "status_delta": deltas,
    }


def cmd_diff(a, b, out=None):
    res = diff_snapshots(a, b)
    print(f"[track_diff] A={res['n_a']} NCTs, B={res['n_b']} NCTs")
    print(f"[track_diff] added={res['added']} removed={res['removed']} "
          f"status_change={res['status_change']} spelling_change={res['spelling_change']} "
          f"phase_change={res['phase_change']} sponsor_change={res['sponsor_change']} "
          f"conditions_change={res['conditions_change']}")
    for d in res["status_delta"]:
        ct = d['change_type']
        if ct in ('added', 'removed'):
            print(f"  {ct:<14} {d['nct']}")
        elif ct in ('status_change', 'spelling_change'):
            print(f"  {ct:<14} {d['nct']}: {d['old_status']} -> {d['new_status']}")
        elif ct == 'phase_change':
            print(f"  {ct:<14} {d['nct']}: {d['old_phase']} -> {d['new_phase']}")
        elif ct == 'sponsor_change':
            print(f"  {ct:<14} {d['nct']}: {d['old_sponsor']} -> {d['new_sponsor']}")
        elif ct == 'conditions_change':
            print(f"  {ct:<14} {d['nct']}: jaccard={d['jaccard_similarity']} "
                  f"+{d['added_conditions']} -{d['removed_conditions']}")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print(f"[track_diff] wrote {out}")
    return res


def cmd_track(normalized_path, snapshot_path):
    shutil.copy(normalized_path, snapshot_path)
    print(f"[track_diff] snapshot written -> {snapshot_path} "
          f"(copied from {normalized_path})")


def main():
    ap = argparse.ArgumentParser(
        description="Local status diff / snapshot track for ct-registry (no network)")
    ap.add_argument("--diff", nargs=2, metavar=("SNAP_A", "SNAP_B"),
                    help="diff two normalized.json snapshots by NCT set -> status_delta")
    ap.add_argument("--diff-out", help="write the status_delta JSON here")
    ap.add_argument("--track", help="normalized.json path to snapshot as registry_snapshot.json")
    ap.add_argument("--snapshot-out", default="registry_snapshot.json",
                    help="target snapshot path for --track (default registry_snapshot.json)")
    args = ap.parse_args()
    if args.diff:
        cmd_diff(args.diff[0], args.diff[1], args.diff_out)
    elif args.track:
        cmd_track(args.track, args.snapshot_out)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
