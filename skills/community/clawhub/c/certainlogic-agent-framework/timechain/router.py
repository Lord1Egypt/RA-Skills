#!/usr/bin/env python3
"""
Router — recall-first turn economics (v3.14).

DOCTRINE: wearing the skill is 100% and non-negotiable, and it must SAVE tokens,
not spend them. The model is the FALLBACK, not the default. Every turn routes
through this decision BEFORE any model reasoning:

    REPLAY   a sealed antecedent already answers this (Brain replay or
             replay.match above threshold) -> confirm it, seal a replay-grounded
             ring, spend ~zero model tokens on regeneration.
    PARTIAL  the chain holds substantial relevant context (hippocampus recall)
             but no full antecedent -> the model reasons ONLY over the missing
             delta; the found rings are the evidence base (--used-rings them).
    MODEL    novel ground: cambium detects a genuine faculty gap (dissonance
             above floor) or recall finds nothing usable -> full model
             reasoning is REQUIRED; growth may fire to cover the gap.

    ROUTING ORDER: Brain REPLAY > Brain Bridge > Timechain REPLAY >
    Timechain hippocampus > Archive API > Cambium gap > MODEL.
    Brain is PRIMARY; archive is secondary; model is fallback.

Usage (the first command of every turn):

    python3 router.py route "<the user's request>" [--context "..."] [--json]

Output: the decision, the evidence (antecedent ring / recalled rings / gap
report), and the exact next command to run. Telemetry logs every routing
decision so the savings are measurable (`python3 router.py stats`).

Stdlib only. Python 3.8+. Builds on replay.py, hippocampus.py, cambium.py,
telemetry.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))

import telemetry as telem
import faculties

# PARTIAL requires this much lexical relevance mass across recalled rings.
# v3.15: read THROUGH the calibrators registry — dream.calibrate_router owns
# these and adjusts them from route_regret evidence (bounded, sealed).
try:
    import calibrators as _cal
    PARTIAL_FLOOR = float(_cal.get("router.partial_floor", 0.35))
    PARTIAL_RINGS = int(_cal.get("router.partial_rings", 2))
except Exception:
    PARTIAL_FLOOR = 0.35      # top recalled ring score floor
    PARTIAL_RINGS = 2         # need at least this many related rings

# Faculties auto-register built-in senses on import.
# Session-gen faculties persist in faculties._GENERATED_SESSION.

# Modality detection: keyword sets per mode
_MODALITY_SIGS = {
    "coding": {"code", "script", "function", "api", "bug", "debug",
                "test", "compile", "syntax", "type", "class", "def",
                "import", "error", "lint", "build", "deploy", "pytest",
                "module", "package", "import"},
    "executive": {"strategy", "business", "plan", "product", "market",
                   "scope", "build", "approve", "decision", "funding",
                   "partner", "launch", "pipeline", "revenue"},
    "creative": {"design", "create", "imagine", "write", "draft",
                  "explore", "brainstorm", "generate", "compose"},
    "metacognitive": {"why", "reflect", "learn", "improve", "meta",
                       "self", "how do i", "how should", "regret"},
}
_MODALITY_WEIGHTS = {
    "cognitive": {"jaccard": 1.0, "query_coverage": 1.0, "bm25_rank": 0.5, "score_boost": 0.0},
    "coding":    {"jaccard": 0.7, "query_coverage": 1.0, "bm25_rank": 0.8, "score_boost": 0.5},
    "executive": {"jaccard": 0.8, "query_coverage": 1.0, "bm25_rank": 0.3, "score_boost": 0.0},
    "creative":  {"jaccard": 0.5, "query_coverage": 0.5, "bm25_rank": 0.3, "score_boost": 0.0},
}


def _detect_modality(query: str) -> str:
    """Auto-detect cognitive modality from query lexicon.

    Priority: keyword matches > cambium faculty orientation > cognitive fallback.
    Cambium's infer_kind returns registry kinds ('sense'/'modality') not cognitive
    modes — we use it as a secondary signal only.
    """
    qs = set(query.lower().split())
    _best, _best_score = "cognitive", 0
    for _mod, _sigs in _MODALITY_SIGS.items():
        _overlap = len(qs & _sigs)
        if _overlap > _best_score:
            _best, _best_score = _mod, _overlap
    # Use cambium as a tiebreaker or cross-check
    try:
        import cambium
        if hasattr(cambium, "faculty_orientation"):
            _orient = cambium.faculty_orientation(_best)
            if _orient:
                pass  # orientation enriches but doesn't override keyword match
    except Exception:
        pass
    return _best


def _apply_modality_weights(modality: str):
    """Adjust faculty weights for the detected modality."""
    _w = _MODALITY_WEIGHTS.get(modality, _MODALITY_WEIGHTS["cognitive"])
    for _name, _weight in _w.items():
        _f = faculties.get_faculty(_name, "sense")
        if _f:
            _f["weight"] = _weight


def _load_env_key(var_name):
    """Load a key from env or .brain_env fallback."""
    key = os.environ.get(var_name)
    if key:
        return key
    try:
        _be = Path(__file__).resolve().parent.parent.parent / ".brain_env"
        if _be.exists():
            for _line in _be.read_text().splitlines():
                if _line.startswith(f"export {var_name}="):
                    _parts = _line.strip().split("=", 1)
                    if len(_parts) == 2:
                        _v = _parts[1].strip('"').strip("'\n")
                        os.environ[var_name] = _v
                        return _v
    except Exception:
        pass
    return None


def _api_key():
    """Load INTERNAL_API_KEY from env or .brain_env fallback."""
    return _load_env_key("INTERNAL_API_KEY")


    """Query archive timechain API (462K rings) via HTTP."""
    import urllib.request as _ur
    _url = "http://127.0.0.1:8080/replay"
    _req = _ur.Request(
        _url,
        data=json.dumps({"query": q, "top": t}).encode(),
        headers={"Content-Type": "application/json"}
    )
    if api_key:
        _req.add_header("X-API-Key", api_key)
    try:
        with _ur.urlopen(_req, timeout=3) as _resp:
            _data = json.loads(_resp.read())
            _results = _data.get("candidates", [])
            return [
                {"ring": r.get("index") or r.get("rowid") or i,
                 "score": round(float(r.get("score", 0.5)), 3),
                 "source": "archive-api",
                 "summary": (r.get("summary") or r.get("snippet") or "")[:150]}
                for i, r in enumerate(_results[:t])
            ] if _results else []  # empty list = no error, just no hits
    except Exception:
        return None



def _search_brain_bridge(query, api_key):
    """Query Brain Bridge (cached facts -> timechain fallback)."""
    import subprocess as _bb_sp
    _bb_script = Path(__file__).resolve().parent.parent.parent / "scripts" / "brain_bridge.py"
    if not _bb_script.exists():
        return None
    try:
        _bb_proc = _bb_sp.run(
            [sys.executable, str(_bb_script), "query", query[:300]],
            capture_output=True, text=True, timeout=4,
            env={"INTERNAL_API_KEY": api_key or "",
                 **{k: v for k, v in os.environ.items()}}
        )
        if _bb_proc.returncode == 0:
            return json.loads(_bb_proc.stdout)
    except Exception:
        pass
    return None


def route(root: Path, query: str, context: str = "", top: int = 5, data_root: Path = None) -> dict:
    # Auto-detect archive root from env var if not passed explicitly.
    if data_root is None:
        _archive = os.environ.get("CT_ARCHIVE_ROOT", "").strip()
        if _archive:
            data_root = Path(_archive)
    root = Path(root)
    out = {"query": query[:200], "decision": None, "evidence": {}, "next": None}
    # Auth key for Brain API
    _API_KEY = _api_key()

    # ---- 0. AUTONOMOUS MODALITY DETECTION ----
    modality = _detect_modality(query)
    _apply_modality_weights(modality)
    out["evidence"]["modality"] = modality
    # Store last rings for faculty generation evaluation
    faculties._GENERATED_SESSION["_last_modality"] = modality

    # ---- 1. BRAIN REPLAY: Brain's continuity module is PRIMARY routing. ---
    # Brain has 68K facts with hippocampus index, PoQ gate, and replay matching.
    # This is the authority; timechain is the cold archive fallback.
    try:
        import urllib.request
        _brain_url = os.environ.get("BRAIN_API_URL", "http://127.0.0.1:8000")
        _encoded = urllib.request.quote(query[:500])
        _br_req = urllib.request.Request(f"{_brain_url}/replay?q={_encoded}")
        _br_key = _API_KEY
        if _br_key:
            _br_req.add_header("X-API-Key", _br_key)
        with urllib.request.urlopen(_br_req, timeout=3) as _resp:
            _br_res = json.loads(_resp.read())

        if _br_res.get("decision") in ("REPLAY", "PARTIAL"):
            out["decision"] = _br_res["decision"]
            out["evidence"]["brain_replay"] = _br_res.get("evidence", {})
            _ant = _br_res.get("evidence", {}).get("antecedent", {})
            if _ant:
                _key = _ant.get("key", "?")
                _score = _ant.get("score", 0)
                out["next"] = (f"Brain REPLAY on fact '{_key}' (score {_score}). "
                               f"Confirm the fact is current, then seal using it as evidence. "
                               f"Do NOT regenerate the answer.")
            else:
                _keys = _br_res.get("evidence", {}).get("partial_keys", [])
                out["next"] = (f"Brain PARTIAL: facts {_keys} provide context. "
                               f"Reason ONLY over the missing delta.")
            _log(root, out, None)
            return out

        out["evidence"]["brain_replay"] = {
            "decision": _br_res.get("decision"),
            "note": "Brain returned MODEL — checking timechain archive"
        }
    except Exception as _bre:
        out["evidence"]["brain_replay_error"] = str(_bre)[:120]

    # ---- 1b. BRAIN BRIDGE: fast cached-fact layer before archive -------------
    # Only reached if Brain API returned MODEL or was unreachable.
    # Queries Brain Bridge (Brain facts cache -> timechain fallback).
    _bb_res = _search_brain_bridge(query, _API_KEY)
    if _bb_res:
        _bb_hit = _bb_res.get("found") or _bb_res.get("answer")
        if _bb_hit and _bb_res.get("confidence", 0) >= 0.6:
            out["decision"] = "PARTIAL"
            out["evidence"]["brain_bridge"] = {
                "source": _bb_res.get("source", "brain-bridge"),
                "summary": str(_bb_hit)[:200],
                "confidence": _bb_res.get("confidence"),
            }
            out["next"] = ("Brain Bridge has a cached answer for this query. "
                           "Use it as context; reason only over the delta.")
            _log(root, out, None)
            return out
        out["evidence"]["brain_bridge"] = {
            "found": False, "confidence": _bb_res.get("confidence", 0)}

    # ---- 1c. TIMEHCHEIN REPLAY: cold archive fallback ---------------------
    # Only reached if Brain returned MODEL or was unreachable.
    try:
        import replay
        eng = replay.Replay(root) if hasattr(replay, "Replay") else None
        if eng is not None:
            m = eng.match(query, context=context, top=top)
        else:
            m = replay.match(root, query, context=context, top=top)
        cands = m.get("candidates") or m.get("matches") or []
        thr = m.get("threshold") or 0.55
        best = cands[0] if cands else None
        if best and float(best.get("score", 0)) >= float(thr):
            out["decision"] = "REPLAY"
            out["evidence"]["antecedent"] = {
                "ring": best.get("index") or best.get("ring"),
                "score": best.get("score"),
                "summary": (best.get("summary") or "")[:200],
            }
            ring_id = best.get("index") or best.get("ring")
            out["next"] = (f"Confirm the antecedent answers the request, then: "
                           f"python3 replay.py accept --ring {ring_id} "
                           f"(or reject if it does not fit — rejects tune the threshold). "
                           f"Seal grounds on ring {ring_id}; do NOT regenerate the answer.")
            _log(root, out, thr)
            return out
        out["evidence"]["replay_best"] = ({"ring": best.get("index") or best.get("ring"),
                                           "score": best.get("score")} if best else None)
    except Exception as exc:
        out["evidence"]["replay_error"] = str(exc)[:120]

    # ---- 2. PARTIAL: does the chain hold substantial relevant context? (parallel) -----
    # Queries 2 sources in parallel: identity chain, archive file
    import concurrent.futures
    from timechain import Timechain
    from poq import tokens as _toks

    def _search_identity(r, q, ctx, t):
        import hippocampus as hip
        hits = hip.Hippocampus(r).search(q, context=ctx)[:t]
        result = []
        idxs = []
        for h in hits:
            if isinstance(h, dict):
                result.append({"ring": h.get("index"),
                               "score": round(float(h.get("score", 0)), 3),
                               "source": "identity-chain",
                               "summary": (h.get("summary") or h.get("text") or "")[:150]})
            else:
                idxs.append(int(h))
        if idxs:
            tc = Timechain(r)
            texts = {}
            for i in idxs:
                ring = tc.ring_by_index(i)
                if ring is None:
                    continue
                p = ring.get("payload") or ring.get("content") or {}
                if isinstance(p, dict):
                    texts[i] = (p.get("summary") or p.get("objective")
                                or p.get("function") or json.dumps(p)[:300])
                else:
                    texts[i] = str(p)[:300]
            for i in idxs:
                result.append({"ring": i,
                               "score": 0.5,
                               "source": "identity-chain",
                               "summary": (texts.get(i) or "")[:150]})
        # Faculty sense fusion replaces rudimentary Jaccard-only scoring
        if result:
            result = faculties.fuse_senses(q, result)
            faculties._GENERATED_SESSION["_last_rings"] = result
        return result

    def _search_archive(dr, q, ctx, t):
        # Fast path: FTS5 index (sub-100ms vs 6s+ hippocampus scan)
        _ws = Path(__file__).resolve().parents[2]
        _dr_abs = Path(str(dr)) if Path(str(dr)).is_absolute() else (_ws / Path(str(dr))).resolve()
        fts5_path = _dr_abs / "fts5.db"
        if fts5_path.exists():
            try:
                import subprocess as _sp
                _arc_recall = _ws / "scripts" / "archive_recall.py"
                if _arc_recall.exists():
                    _proc = _sp.run(
                        [sys.executable, str(_arc_recall), "--fts5", str(fts5_path),
                         "query", q, "--limit", str(t), "--json"],
                        capture_output=True, text=True, timeout=5,
                    )
                    if _proc.returncode == 0:
                        _data = json.loads(_proc.stdout)
                        _results = _data.get("results", [])
                        return [
                            {"ring": r["rowid"],
                             "score": round(1.0 - (idx / max(len(_results), 1)), 3),
                             "source": "archive-file",
                             "summary": r.get("snippet", "")[:150]}
                            for idx, r in enumerate(_results)
                        ]
            except Exception:
                pass
        return _search_identity(dr, q, ctx, t)

    recalled = []
    arch_recalled = []
    arch_ok = True

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    try:
        id_future = pool.submit(_search_identity, root, query, context, top)
        arch_future = None
        if data_root is not None:
            dr = Path(data_root) if isinstance(data_root, str) else data_root
            arch_future = pool.submit(_search_archive, dr, query, context, top)
        try:
            recalled = id_future.result(timeout=5)
        except Exception:
            import hippocampus as hip
            try:
                hits = hip.Hippocampus(root).search(query, context=context)[:top]
                for h in hits:
                    if isinstance(h, dict):
                        recalled.append({"ring": h.get("index"),
                                         "score": round(float(h.get("score", 0)), 3)})
                    else:
                        recalled.append({"ring": int(h), "score": 0.5})
            except:
                pass

        if arch_future is not None:
            try:
                arch_recalled = arch_future.result(timeout=2.0)
            except concurrent.futures.TimeoutError:
                arch_ok = False
                out["evidence"]["archive_timeout"] = True
            except Exception as exc:
                out["evidence"]["archive_error"] = str(exc)[:120]

    finally:
        pool.shutdown(wait=False)

    out["evidence"]["recalled"] = recalled[:top]
    if arch_recalled:
        out["evidence"]["archive_recalled"] = arch_recalled[:top]
    if not arch_ok:
        out["decision"] = "PARTIAL"
        out["evidence"]["partial_reason"] = "Archive timed out (2s), using identity + model"

    # Merge identity + archive file results for PARTIAL decision
    _all_candidates = list(recalled)
    if arch_recalled:
        for r in arch_recalled:
            if r not in _all_candidates:
                _all_candidates.append(r)
    _all_candidates.sort(key=lambda r: r["score"], reverse=True)

    strong = [r for r in _all_candidates if r["score"] >= PARTIAL_FLOOR]
    out["evidence"]["recalled"] = recalled

    # ---- 3. Gap check: does cambium flag a genuine faculty gap? ------------
    gap = None
    try:
        import cambium
        home = cambium.registry_home(root, None)
        gap = cambium.detect_gap(cambium.load_corpus(home), query, context)
        out["evidence"]["gap"] = {"dissonance": gap["dissonance"],
                                  "coverage": gap["coverage_ratio"],
                                  "uncovered": gap["uncovered"][:6]}
    except Exception as exc:
        out["evidence"]["gap_error"] = str(exc)[:120]

    gap_flagged = bool(gap and gap["dissonance"] > cambium.DISSONANCE_FLOOR)

    # Strong context from identity chain or archive wins.
    # The model reasons only over the missing delta.
    if len(strong) >= PARTIAL_RINGS:
        out["decision"] = "PARTIAL"
        ids = [str(r.get("ring", r.get("id", r.get("key", "?")))) for r in strong]
        gap_note = (" Cambium flags a gap — growth will fire on seal." if gap_flagged else "")
        sources = ", ".join(sorted(set(r.get("source", "?") for r in strong)))
        out["next"] = (f"Recalled from {sources}: rings {', '.join(ids)} as evidence base; "
                       f"reason ONLY over what they do not cover; "
                       f"seal with --used-rings {' '.join(ids)}." + gap_note)
    else:
        out["decision"] = "MODEL"
        why = ("cambium flags a faculty gap (dissonance "
               f"{gap['dissonance']})" if gap_flagged else
               "no sealed antecedent and insufficient chain context")
        out["evidence"]["why_model"] = why

        # --- IN-SESSION FACULTY GENERATION (synchronous, best-effort) ---
        # When the router hits MODEL on a genuine gap, generate a new
        # registered faculty that catches this topic. Runs inline on MODEL
        # path (already the slow path — acceptable overhead).
        try:
            _genned = faculties.generate_faculty(gap or {}, query, context)
            if _genned.get("kept"):
                out["evidence"]["generated_faculty"] = {
                    "name": _genned["name"],
                    "eval_score": _genned["eval_score"],
                    "source": "autogen",
                }
                out["next"] = (
                    f"Model reasoning + generated faculty '{_genned['name']}' "
                    f"(eval={_genned['eval_score']}) to fill gap. "
                    f"Run the loop: python3 recall.py turn \"<thought>\" "
                    f"--input \"<request>\" — growth will fire if genuine.")
            else:
                out["next"] = (
                    "Full model reasoning required (no usable faculty "
                    "could be generated). Run the loop: "
                    "python3 recall.py turn \"<thought>\" "
                    "--input \"<request>\" — growth will fire if genuine.")
        except Exception:
            out["next"] = (
                "Full model reasoning required (" + why + "). Run the loop: "
                "python3 recall.py turn \"<thought>\" --input \"<request>\" — "
                "growth will fire if the gap is genuine.")

    _log(root, out, None)
    return out


def _log(root, out, threshold):
    try:
        telem.record(str(root), "route_decision", {
            "decision": out["decision"],
            "replay_threshold": threshold,
            "n_recalled": len(out["evidence"].get("recalled") or []),
            "gap": (out["evidence"].get("gap") or {}).get("dissonance"),
        })
    except Exception:
        pass


def cmd_route(args):
    res = route(args.root, args.query, context=args.context or "", top=args.top,
                data_root=getattr(args, "data_root", None))
    if args.json:
        print(json.dumps(res, indent=2))
        return
    print(f"ROUTE: {res['decision']}")
    ev = res["evidence"]
    if res["decision"] == "REPLAY":
        a = ev["antecedent"]
        print(f"  antecedent: ring {a['ring']} (score {a['score']})")
        print(f"  \"{a['summary']}\"")
    else:
        for r in (ev.get("recalled") or [])[:5]:
            print(f"  {r.get('source','?')} #{r['ring']} ({r['score']}): {r['summary'][:90]}")
        if ev.get("archive_recalled"):
            print(f"  archive: {len(ev['archive_recalled'])} hits")
        if ev.get("archive_error"):
            print(f"  archive error: {ev['archive_error']}")
        if ev.get("gap"):
            g = ev["gap"]
            print(f"  gap: dissonance {g['dissonance']} coverage {g['coverage']} "
                  f"uncovered {g['uncovered']}")
    print(f"  NEXT: {res['next']}")


def regret(root: Path, decision_ring: int, verdict: str, why: str = "") -> dict:
    """v3.15: score a past routing decision so thresholds can LEARN.
    verdict: 'over-replay'  (REPLAY/PARTIAL chosen but the answer was wrong/stale
                             -> floor too low),
             'over-model'   (MODEL chosen but the chain had it -> floor too high),
             'good'         (decision was right — reinforces current thresholds)."""
    if verdict not in ("over-replay", "over-model", "good"):
        raise SystemExit("verdict must be over-replay|over-model|good")
    telem.record(str(root), "route_regret",
                 {"ring": decision_ring, "verdict": verdict, "why": why[:200]})
    return {"ring": decision_ring, "verdict": verdict}


def cmd_regret(args):
    r = regret(args.root, args.ring, args.verdict, args.why or "")
    print(f"regret recorded for routing at ring {r['ring']}: {r['verdict']} "
          f"(dream.calibrate_router learns from these)")


def cmd_stats(args):
    from collections import Counter
    c, n = Counter(), 0
    try:
        for _, e in telem.Telemetry(args.root).events():
            if e.get("event") == "route_decision":
                c[(e.get("data") or {}).get("decision", "?")] += 1
                n += 1
    except Exception:
        pass
    print(f"route decisions: {n}")
    for k, v in c.most_common():
        pct = (v / n * 100) if n else 0
        print(f"  {k:<8} {v}  ({pct:.0f}%)")
    if n:
        saved = c.get("REPLAY", 0) + c.get("PARTIAL", 0)
        print(f"  model-avoidance rate: {saved / n * 100:.0f}% "
              f"(REPLAY answered from chain; PARTIAL reasoned only the delta)")


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=SKILL_DIR)
    ap = argparse.ArgumentParser(description="Recall-first turn router", parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("route", parents=[common],
                        help="decide REPLAY | PARTIAL | MODEL for a request")
    pr.add_argument("query")
    pr.add_argument("--context", default="")
    pr.add_argument("--top", type=int, default=5)
    pr.add_argument("--data-root", type=Path, default=None,
                    help="Additional archive chain for historical recall")
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_route)
    ps = sub.add_parser("stats", parents=[common],
                        help="routing decision distribution + model-avoidance rate")
    ps.set_defaults(func=cmd_stats)
    pg = sub.add_parser("regret", parents=[common],
                        help="score a past route decision")
    pg.add_argument("ring", type=int)
    pg.add_argument("verdict", choices=["over-replay", "over-model", "good"])
    pg.add_argument("--why", default="")
    pg.set_defaults(func=cmd_regret)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()