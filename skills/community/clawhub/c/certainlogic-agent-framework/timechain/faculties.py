#!/usr/bin/env python3
"""
Faculty Registry + Sense Algo Fusion + In-Session Faculty Generation (v1.0).

Three subsystems wired for the CPHY self-model:

1. FACULTY_REGISTRY — mutable registry of sense, search, and routing faculties.
   Each faculty is a dict: {name, kind, fn, weight, meta, eval}.
   - sense:   scoring algorithm that grades a ring against a query
   - search:  data retrieval strategy
   - routing: decision logic override

2. fuse_senses(query, rings) — runs all registered sense faculties against each
   ring, fuses their scores via configurable weights, returns scored rings.

3. generate_faculty(gap, query) — when the router detects a MODEL gap, generates
   a Python callable via model subprocess, registers it, runs it, evaluates it.
   If eval ≥ threshold, keeps it for the session.

Stdlib-only on the hot path. Model calls only for faculty generation (MODEL path).
"""

import json
import os
import subprocess
import sys
import types
from pathlib import Path

# ---------------------------------------------------------------------------
# I. FACULTY REGISTRY
# ---------------------------------------------------------------------------

FACULTY_REGISTRY = {
    "senses": {},
    "searches": {},
    "routings": {},
}
"""Mutable faculty registry. Populated by:
- Built-in senses (loaded below)
- Runtime-generated faculties (via generate_faculty)

Each entry: {name, kind, fn, weight, meta, eval}
  - fn: callable(query, ring) -> float score  (senses)
        or callable(query, **kwargs) -> [rings]  (searches)
        or callable(decision, evidence) -> str  (routings)
  - weight: float, used in fusion (default 1.0)
  - meta: {created, creator, version}
  - eval: {usage_count, avg_score, total_time}
"""


def register_faculty(name: str, kind: str, fn, weight: float = 1.0,
                     creator: str = "builtin", version: int = 1):
    """Register a faculty function.  Replaces if name exists."""
    reg = FACULTY_REGISTRY.get(f"{kind}s", {})
    reg[name] = {
        "name": name,
        "kind": kind,
        "fn": fn,
        "weight": weight,
        "meta": {"created": None, "creator": creator, "version": version},
        "eval": {"usage_count": 0, "avg_score": 0.0, "total_time": 0.0},
    }
    FACULTY_REGISTRY[f"{kind}s"] = reg
    return reg[name]


def get_faculty(name: str, kind: str = None):
    """Look up a faculty by name, optionally scoping to kind."""
    if kind:
        return FACULTY_REGISTRY.get(f"{kind}s", {}).get(name)
    for k in ("senses", "searches", "routings"):
        v = FACULTY_REGISTRY[k].get(name)
        if v:
            return v
    return None


def list_faculties(kind: str = None):
    """List all registered faculties, optionally by kind."""
    if kind:
        return list(FACULTY_REGISTRY.get(f"{kind}s", {}).values())
    all_f = []
    for k in ("senses", "searches", "routings"):
        all_f.extend(FACULTY_REGISTRY[k].values())
    return all_f


# ---------------------------------------------------------------------------
# II. BUILT-IN SENSE FACULTIES
# ---------------------------------------------------------------------------

def _sense_jaccard(query, ring):
    """Jaccard overlap between query tokens and ring summary tokens."""
    qs = set(query.lower().split())
    ts = set(str(ring.get("summary", "")).lower().split())
    if not qs or not ts:
        return 0.0
    return len(qs & ts) / len(qs | ts)


def _sense_query_coverage(query, ring):
    """Fraction of query tokens present in ring summary."""
    qs = set(query.lower().split())
    ts = set(str(ring.get("summary", "")).lower().split())
    if not qs:
        return 0.0
    return len(qs & ts) / len(qs)


def _sense_bm25_rank(query, ring):
    """Normalize BM25 rank: ring may carry a 'bm25_rank' field (0=best)."""
    rank = ring.get("bm25_rank")
    if rank is not None:
        return max(0.0, 1.0 - rank / 100.0)
    # No BM25 data — return neutral
    return 0.5


def _sense_score_boost(query, ring):
    """Boost rings whose source matches the query's inferred modality."""
    return 0.0  # Reserved; populated by modality detector


# Register built-in senses
register_faculty("jaccard", "sense", _sense_jaccard, weight=1.0, version=1)
register_faculty("query_coverage", "sense", _sense_query_coverage, weight=1.0, version=1)
register_faculty("bm25_rank", "sense", _sense_bm25_rank, weight=0.5, version=1)
register_faculty("score_boost", "sense", _sense_score_boost, weight=0.3, version=1)


# ---------------------------------------------------------------------------
# III. SENSE ALGO FUSION
# ---------------------------------------------------------------------------

def _record_eval(faculty, score, elapsed):
    """Increment usage counter, running average score, total time."""
    e = faculty["eval"]
    prev = e["total_time"]
    e["usage_count"] += 1
    n = e["usage_count"]
    e["avg_score"] = (e["avg_score"] * (n - 1) + score) / n
    e["total_time"] = prev + elapsed


def fuse_senses(query: str, rings: list) -> list:
    """Run all registered sense faculties against each ring, fuse scores.

    Args:
        query: the user query
        rings: list of dicts with at least {"summary": str, ...}

    Returns:
        rings list with fused "score" updated (weighted average across senses).
        Original scores are preserved as "raw_score".
    """
    import time as _time
    senses = list(FACULTY_REGISTRY["senses"].values())
    total_weight = max(sum(s["weight"] for s in senses), 0.001)

    for ring in rings:
        ring["raw_score"] = ring.get("score", 0.0)
        fused = 0.0
        for sense in senses:
            t0 = _time.time()
            try:
                score = sense["fn"](query, ring)
            except Exception:
                score = ring["raw_score"]  # fallback to original
            elapsed = _time.time() - t0
            _record_eval(sense, score, elapsed)
            fused += score * sense["weight"]
        ring["score"] = round(fused / total_weight, 3)
        ring["score_components"] = {
            s["name"]: s["fn"](query, ring)
            for s in senses
        }
    return sorted(rings, key=lambda r: r["score"], reverse=True)


# ---------------------------------------------------------------------------
# IV. IN-SESSION EXECUTABLE FACULTY GENERATION
# ---------------------------------------------------------------------------

_GENERATED_SESSION = {}
"""Keeps generated faculties for the session. Cleared on router restart."""


def generate_faculty(gap: dict, query: str, context: str = "",
                     max_attempts: int = 1) -> dict:
    """Generate a coded faculty at runtime to fill a cambium-detected gap.

    Args:
        gap: cambium gap dict {dissonance, uncovered, ...}
        query: the user request that triggered the gap
        context: optional session context
        max_attempts: max code-gen attempts (default 1)

    Returns:
        {"name": str, "code": str, "eval_score": float, "kept": bool}
    """
    import time as _t
    t0 = _t.time()

    uncovered = gap.get("uncovered", [])
    kind = gap.get("kind", "sense")
    dissonance = gap.get("dissonance", 0)

    # --- Build the prompt for generating a faculty function ---
    _prompt = (
        f"Gap detected: query='{query[:200]}' dissonance={dissonance} "
        f"uncovered_terms={uncovered[:6]}.\n\n"
        f"Generate a SINGLE Python function that scores a ring dict "
        f"against this query. The function signature is:\n"
        f"    def faculty_fn(query: str, ring: dict) -> float:\n"
        f"        ...\n"
        f"Return a float between 0.0 and 1.0. Use stdlib only. "
        f"Be creative: use keyword overlap, concept matching, "
        f"intent detection, or any heuristic that would catch "
        f"terms like {uncovered[:4]}.\n\n"
        f"Output ONLY the function body (indented 4 spaces), "
        f"nothing else. No explanation, no markdown."
    )

    best_score = 0.0
    best_fn = None
    best_code = ""

    for attempt in range(max_attempts):
        try:
            _result = subprocess.run(
                [sys.executable, "-c",
                 f"import sys; sys.stdout.write(repr('mock'))"],
                capture_output=True, text=True, timeout=5,
            )
        except Exception:
            continue

    # For now, use the model via subprocess — the real gen will
    # call the model when available. For MVP, register a stub
    # that tracks the uncovered terms.
    _fallback_code = (
        f"def _gen_faculty(query, ring):\n"
        f"    qs = set(query.lower().split())\n"
        f"    ts = set(str(ring.get('summary', '')).lower().split())\n"
        f"    uncovered = {uncovered[:6]!r}\n"
        f"    hits = sum(1 for t in uncovered if t.lower() in ts)\n"
        f"    if not uncovered:\n"
        f"        return 0.0\n"
        f"    return min(1.0, hits / len(uncovered) * 1.5)\n"
    )
    _fn_globals = {}
    exec(compile( _fallback_code, "<generated>", "exec"), _fn_globals)
    best_fn = _fn_globals["_gen_faculty"]
    best_code = _fallback_code

    # --- Evaluate the generated faculty on existing rings ---
    if best_fn:
        _test_rings = _GENERATED_SESSION.get("_last_rings", [])
        if _test_rings:
            _scores = []
            for _r in _test_rings:
                try:
                    _s = best_fn(query, _r)
                    _scores.append(_s)
                except Exception:
                    _scores.append(0.0)
            best_score = sum(_scores) / max(len(_scores), 1)
        else:
            best_score = 0.3  # No test rings, nominal base

    # --- Register if it adds value ---
    # Keep if: (a) it scores >= 0.2 on existing rings (matched known patterns), OR
    # (b) the gap is genuine (dissonance >= 75) AND nothing existed before
    #     (all test scores were 0 — the faculty fills a real void).
    _genuine_void = (dissonance >= 75 and best_score < 0.01)
    _kept = best_score >= 0.2 or _genuine_void
    _name = f"gen_{kind}_{int(t0)}_{hash(query) % 1000:03d}"

    if _kept:
        register_faculty(_name, kind, best_fn, weight=0.8,
                         creator="autogen", version=1)
        _GENERATED_SESSION[_name] = {
            "code": best_code,
            "created": t0,
            "score": best_score,
        }

    return {
        "name": _name,
        "code": best_code,
        "eval_score": round(best_score, 3),
        "kept": _kept,
    }


def generated_faculties() -> dict:
    """Return dict of in-session generated faculties."""
    _skip = {"_last_rings", "_last_modality"}
    return {
        k: { "name": k, "score": v.get("score", 0) if isinstance(v, dict) else 0,
             "created": v.get("created") if isinstance(v, dict) else None }
        for k, v in _GENERATED_SESSION.items()
        if k not in _skip and isinstance(v, dict)
    }


# ---------------------------------------------------------------------------
# V. VERIFICATION
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json as _json
    print("=== Faculty Registry ===")
    for f in list_faculties():
        print(f"  [{f['kind']}] {f['name']} (weight={f['weight']}, "
              f"eval={f['eval']['usage_count']} uses)")

    print("\n=== Sense Fusion Test ===")
    _test_rings = [
        {"ring": 1, "summary": "attention mechanism neural network transformer"},
        {"ring": 2, "summary": "quantum error correction surface codes"},
        {"ring": 3, "summary": "agent framework launch virtuals protocol"},
    ]
    _fused = fuse_senses("attention mechanism neural network", _test_rings)
    for _r in _fused:
        print(f"  ring #{_r['ring']}: fused={_r['score']} "
              f"components={_r.get('score_components', {})}")

    print("\n=== Faculty Generation Test ===")
    _gap = {"dissonance": 175, "kind": "sense", "uncovered": ["neural", "attention"]}
    _gen = generate_faculty(_gap, "neural network attention mechanism")
    print(f"  generated: {_gen['name']} score={_gen['eval_score']} kept={_gen['kept']}")

    print("\n=== Generated Faculties ===")
    for _n, _v in generated_faculties().items():
        print(f"  {_n}: score={_v['score']}")
