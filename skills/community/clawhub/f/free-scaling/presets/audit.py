#!/usr/bin/env python3
"""Audit preset — run behavioral compliance checks via scale().

Uses the system-audit collector + question generator, pipes everything
through nim_ensemble.scale(k=N) for ensemble judgment.

Usage:
    python3 -m presets.audit                    # k=3 (default)
    python3 -m presets.audit -k 5               # more models
    python3 -m presets.audit --json              # machine-readable
    python3 -m presets.audit --skip-collect      # reuse cached state
"""

import argparse
import json
import os
import re
import sys
import time

# Find the audit scripts
AUDIT_SCRIPTS = os.path.join(
    os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")),
    "skills", "system-audit", "scripts"
)

# Add paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, AUDIT_SCRIPTS)


def extract_patterns(question_text: str) -> list[str]:
    """Extract answer options from 'Answer X, Y, ..., or Z' in question text.

    Handles arbitrary number of comma/or-separated options, with optional
    parenthetical descriptions like 'SAFE (no issues)'.
    """
    # Match "Answer <options>" — options are comma/or-separated labels
    # with optional parenthetical descriptions
    m = re.search(
        r'[Aa]nswer\s+'
        r'([\w_-]+(?:\s*\([^)]*\))?'                           # first option
        r'(?:(?:,\s*(?:or\s+)?|\s+or\s+)[\w_-]+(?:\s*\([^)]*\))?)*)',  # rest
        question_text
    )
    if not m:
        return []
    # Split on comma (with optional trailing "or") or standalone "or"
    parts = re.split(r',\s*(?:or\s+)?|\s+or\s+', m.group(1))
    labels = []
    for part in parts:
        label = re.match(r'([\w_-]+)', part.strip())
        if label:
            labels.append(label.group(1).upper())
    return labels


def collect_state(timeout_per_job: int = 10):
    """Collect system state using the audit collector."""
    from collect import collect_all
    return collect_all()


def run_audit(k: int = 3, verbose: bool = False, json_output: bool = False,
              state: dict = None, timeout: int = 15, backend: str = "hybrid"):
    """Run the full audit pipeline.
    
    Args:
        k: Number of models per question (NIM mode)
        backend: "nim" (NIM only), "copilot" (Copilot only), or "hybrid" (auto-route)
            hybrid: uses Copilot (cp-4.1 + cp-mini) for behavioral/long questions,
                    NIM scale(k) for short factual/deterministic questions
    """
    from nim_ensemble import scale, call_copilot
    from nim_ensemble.parser import parse_answer
    from questions import generate_questions
    
    t0 = time.time()
    
    # Step 1: Collect
    if state is None:
        if verbose:
            print("Collecting system state...", file=sys.stderr)
        state = collect_state()
    
    # Step 2: Generate questions
    questions = generate_questions(state)
    if verbose:
        print(f"Generated {len(questions)} questions", file=sys.stderr)
    
    # Step 3: Run each through scale(k=)
    results = []
    total_calls = 0
    
    for q in questions:
        qid = q.get("id", "?")
        text = q.get("question_text", "")
        
        if not text:
            continue
        
        # Skip pre-answered (deterministic) questions
        if q.get("pre_answered"):
            results.append({
                "id": qid,
                "category": q.get("category", "?"),
                "answer": q.get("answer", "?"),
                "confidence": 1.0,
                "calls": 0,
                "elapsed_s": 0,
                "source": "deterministic",
                "models": [],
            })
            if not json_output:
                print(f"  [{qid}] {q.get('answer', '?')} (deterministic)")
            continue
        
        # Extract answer patterns from question text
        patterns = extract_patterns(text)
        if not patterns:
            patterns = ["COMPLIANT", "DRIFTING", "VIOLATED"]  # default
        
        # Decide backend for this question
        category = q.get("category", "")
        use_copilot = False
        if backend == "copilot":
            use_copilot = True
        elif backend == "hybrid":
            # Behavioral questions (Q1.x, long context) → Copilot (smarter, 1M context)
            # Operational/deterministic → NIM (fast, diverse)
            use_copilot = category in ("behavioral",) or qid.startswith("Q1.")
        
        try:
            t1 = time.time()
            
            if use_copilot:
                # Copilot voting: cp-4.1 + cp-mini (2 different architectures)
                # Falls back to NIM if Copilot token is expired
                copilot_models = ["cp-4.1", "cp-mini"]
                models_detail = []
                votes_raw = []
                copilot_failed = False
                
                for cm in copilot_models:
                    try:
                        ans, raw = call_copilot(text, cm)
                    except (RuntimeError, Exception) as e:
                        # Any Copilot failure → fall back to NIM
                        copilot_failed = True
                        break
                    if ans == "ERROR":
                        copilot_failed = True
                        break
                    if patterns and ans not in patterns:
                        ans = parse_answer(raw, patterns=patterns)
                    models_detail.append((cm, ans))
                    votes_raw.append(ans)
                    total_calls += 1
                
                if copilot_failed:
                    # Fallback to NIM for this question
                    if not json_output:
                        print(f"  [{qid}] copilot expired, falling back to NIM...", flush=True)
                    result = scale(text, k=k, answer_patterns=patterns)
                    total_calls += result.calls_made
                    models_detail = [(m, a) for m, a, _ in result.votes]
                    dt = time.time() - t1
                    results.append({
                        "id": qid,
                        "category": category,
                        "answer": result.answer,
                        "confidence": result.confidence,
                        "calls": result.calls_made,
                        "elapsed_s": round(dt, 1),
                        "source": f"nim-fallback",
                        "models": models_detail,
                    })
                    if not json_output:
                        ms = ", ".join(f"{m}={a}" for m, a in models_detail)
                        print(f"  [{qid}] {result.answer} ({result.confidence:.0%}, {dt:.1f}s) [nim-fallback] — {ms}")
                    continue
                
                # Majority from copilot votes
                if votes_raw:
                    from collections import Counter
                    counts = Counter(votes_raw)
                    answer, count = counts.most_common(1)[0]
                    confidence = count / len(votes_raw)
                else:
                    answer, confidence = "ERROR", 0
                
                dt = time.time() - t1
                results.append({
                    "id": qid,
                    "category": category,
                    "answer": answer,
                    "confidence": confidence,
                    "calls": len(copilot_models),
                    "elapsed_s": round(dt, 1),
                    "source": "copilot",
                    "models": models_detail,
                })
                
                if not json_output:
                    models_str = ", ".join(f"{m}={a}" for m, a in models_detail)
                    print(f"  [{qid}] {answer} ({confidence:.0%}, {dt:.1f}s) [copilot] — {models_str}")
            
            else:
                # NIM voting via scale(k=)
                result = scale(text, k=k, answer_patterns=patterns)
                total_calls += result.calls_made
                
                models_detail = [(m, a) for m, a, _ in result.votes]
                
                results.append({
                    "id": qid,
                    "category": category,
                    "answer": result.answer,
                    "confidence": result.confidence,
                    "calls": result.calls_made,
                    "elapsed_s": round(result.elapsed_s, 1),
                    "source": f"scale-{k}",
                    "models": models_detail,
                })
                
                if not json_output:
                    conf_str = f"{result.confidence:.0%}"
                    models_str = ", ".join(f"{m}={a}" for m, a in models_detail)
                    print(f"  [{qid}] {result.answer} ({conf_str}, {result.elapsed_s:.1f}s) [nim] — {models_str}")
        
        except Exception as e:
            results.append({
                "id": qid,
                "category": category,
                "answer": "ERROR",
                "confidence": 0,
                "calls": 0,
                "elapsed_s": 0,
                "source": "error",
                "error": str(e),
                "models": [],
            })
            if not json_output:
                print(f"  [{qid}] ERROR: {e}")
    
    elapsed = time.time() - t0
    
    # Summary
    summary = {
        "total_questions": len(results),
        "total_calls": total_calls,
        "elapsed_s": round(elapsed, 1),
        "k": k,
        "by_answer": {},
    }
    for r in results:
        ans = r["answer"]
        summary["by_answer"][ans] = summary["by_answer"].get(ans, 0) + 1
    
    if json_output:
        print(json.dumps({"results": results, "summary": summary}, indent=2))
    else:
        print(format_report(results, summary))
    
    return results, summary


# Answer classification for the report
PASS_ANSWERS = {"COMPLIANT", "FOLLOWED", "HEALTHY", "CLEAN", "CONSISTENT", 
                "EFFICIENT", "RELIABLE", "WITHIN_CAPACITY", "PATCHED", "OK"}
WARN_ANSWERS = {"DRIFTING", "MINOR_DRIFT", "PARTIALLY", "FLAKY", "UNCLEAR",
                "WASTEFUL", "OVER_CAPACITY", "HAS_ISSUES"}
FAIL_ANSWERS = {"VIOLATED", "REPEATING", "FAILING", "INCONSISTENT", "NOT_PATCHED",
                "DEGRADING", "CRITICAL"}


def classify_severity(answer: str) -> str:
    """Classify an answer into OK/WARNING/CRITICAL."""
    a = answer.upper()
    if a in PASS_ANSWERS:
        return "OK"
    if a in FAIL_ANSWERS:
        return "CRITICAL"
    if a in WARN_ANSWERS:
        return "WARNING"
    return "WARNING"  # unknown → warning


def format_report(results: list[dict], summary: dict) -> str:
    """Format a structured audit report."""
    lines = []
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    
    lines.append(f"\n{'='*60}")
    lines.append(f"  SYSTEM AUDIT REPORT")
    lines.append(f"  {ts} | k={summary['k']} | {summary['total_calls']} API calls | {summary['elapsed_s']:.0f}s | $0")
    lines.append(f"{'='*60}")
    
    # Group by severity
    ok, warn, crit, err = [], [], [], []
    for r in results:
        sev = classify_severity(r["answer"])
        if r["answer"] == "ERROR":
            err.append(r)
        elif sev == "OK":
            ok.append(r)
        elif sev == "CRITICAL":
            crit.append(r)
        else:
            warn.append(r)
    
    # Critical first
    if crit:
        lines.append(f"\n🔴 CRITICAL ({len(crit)})")
        lines.append("-" * 40)
        for r in crit:
            conf = f"{r['confidence']:.0%}" if isinstance(r['confidence'], float) else r['confidence']
            models = " ".join(f"{m}={a}" for m, a in r.get("models", []))
            lines.append(f"  [{r['id']}] {r['answer']} ({conf})")
            if models:
                lines.append(f"    votes: {models}")
    
    if warn:
        lines.append(f"\n🟡 WARNING ({len(warn)})")
        lines.append("-" * 40)
        for r in warn:
            conf = f"{r['confidence']:.0%}" if isinstance(r['confidence'], float) else r['confidence']
            models = " ".join(f"{m}={a}" for m, a in r.get("models", []))
            lines.append(f"  [{r['id']}] {r['answer']} ({conf})")
            if models:
                lines.append(f"    votes: {models}")
    
    if ok:
        lines.append(f"\n✅ OK ({len(ok)})")
        lines.append("-" * 40)
        for r in ok:
            conf = f"{r['confidence']:.0%}" if isinstance(r['confidence'], float) else r['confidence']
            lines.append(f"  [{r['id']}] {r['answer']} ({conf})")
    
    if err:
        lines.append(f"\n❌ ERROR ({len(err)})")
        lines.append("-" * 40)
        for r in err:
            lines.append(f"  [{r['id']}] {r.get('error', 'unknown')}")
    
    # Summary bar
    lines.append(f"\n{'='*60}")
    total = len(results)
    lines.append(f"  {total} checks: ✅ {len(ok)} OK | 🟡 {len(warn)} WARNING | 🔴 {len(crit)} CRITICAL | ❌ {len(err)} ERROR")
    
    health = len(ok) / total * 100 if total else 0
    if health >= 80:
        grade = "HEALTHY"
    elif health >= 60:
        grade = "NEEDS ATTENTION"
    else:
        grade = "DEGRADED"
    lines.append(f"  Health: {health:.0f}% — {grade}")
    lines.append(f"{'='*60}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run system audit via scale(k=)")
    parser.add_argument("-k", type=int, default=3, help="Models per question (default 3)")
    parser.add_argument("--backend", "-b", default="hybrid",
                        choices=["nim", "copilot", "hybrid"],
                        help="Backend: nim (NIM only), copilot (Copilot only), hybrid (auto-route, default)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--state", help="Path to cached state JSON")
    args = parser.parse_args()
    
    state = None
    if args.state:
        with open(args.state) as f:
            state = json.load(f)
    
    try:
        run_audit(k=args.k, verbose=args.verbose, json_output=args.json,
                  state=state, backend=args.backend)
    except KeyboardInterrupt:
        sys.exit(130)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
