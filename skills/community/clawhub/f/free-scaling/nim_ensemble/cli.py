#!/usr/bin/env python3
"""CLI for NIM Ensemble — test-time scaling from the command line."""

import argparse
import json
import sys
import time

from . import vote, call_model, MODELS, PANELS, list_models
from . import smart_vote, classify_task, scale


def cmd_scale(args):
    """Scale inference — the core API."""
    patterns = args.answers.split(",") if args.answers else None
    k = args.k if args.k != "auto" else "auto"
    if k != "auto":
        k = int(k)
    
    result = scale(
        args.question,
        k=k,
        answer_patterns=patterns,
        system_prompt=args.system,
    )
    
    if args.json:
        print(json.dumps({
            "answer": result.answer,
            "confidence": result.confidence,
            "k": args.k,
            "calls_made": result.calls_made,
            "stage": result.stage,
            "models": result.models_used,
            "elapsed_s": round(result.elapsed_s, 2),
        }))
    else:
        print(f"{result.answer} (k={args.k}, conf={result.confidence:.0%}, {result.calls_made} calls, {result.elapsed_s:.1f}s)")
        if args.verbose:
            for model, ans, w in result.votes:
                print(f"  {model}: {ans}")
            print(f"  reasoning: {result.reasoning}")


def cmd_smart(args):
    """Smart cascade — capability-aware routing with confidence gating."""
    patterns = args.answers.split(",") if args.answers else None
    result = smart_vote(
        args.question,
        task_type=args.type,
        answer_patterns=patterns,
        system_prompt=args.system,
        confidence_threshold=args.threshold,
        skip_cascade=args.flat,
    )
    
    if args.json:
        print(json.dumps({
            "answer": result.answer,
            "confidence": result.confidence,
            "task_type": result.task_type,
            "stage": result.stage,
            "calls_made": result.calls_made,
            "models": result.models_used,
            "votes": [(m, a, round(w, 2)) for m, a, w in result.votes],
            "elapsed_s": round(result.elapsed_s, 1),
            "reasoning": result.reasoning,
        }, indent=2))
    else:
        print(f"{result.answer} (conf={result.confidence:.0%}, {result.stage}, {result.calls_made} call{'s' if result.calls_made != 1 else ''}, {result.elapsed_s:.1f}s)")
        if args.verbose:
            print(f"  task_type: {result.task_type}")
            for model, ans, weight in result.votes:
                print(f"  {model}: {ans} (weight {weight:.0%})")
            print(f"  reasoning: {result.reasoning}")


def cmd_ask(args):
    """Flat ensemble vote on a single question."""
    patterns = args.answers.split(",") if args.answers else None
    result = vote(
        args.question,
        panel=args.panel,
        system_prompt=args.system,
        answer_patterns=patterns,
        short_circuit=not args.no_short_circuit,
    )
    
    if args.json:
        print(json.dumps({
            "answer": result.answer,
            "confidence": result.confidence,
            "unanimous": result.unanimous,
            "votes": result.votes,
            "models": result.models_used,
            "elapsed_s": round(result.elapsed_s, 1),
            "errors": result.errors,
        }, indent=2))
    else:
        print(f"{result.answer} ({result.confidence})")
        if args.verbose:
            for model, v, raw in zip(result.models_used, result.votes, result.raw_responses):
                print(f"  {model}: {v} — {raw[:120]}")
            print(f"  [{result.elapsed_s:.1f}s]")


def cmd_classify(args):
    """Classify a question's task type."""
    task = classify_task(args.question)
    from .cascade import _DEFAULT_BEST_FOR_TASK, _get_routing
    best_for, _ = _get_routing()
    models = best_for.get(task, _DEFAULT_BEST_FOR_TASK["general"])
    print(f"{task} → {models}")


def cmd_bench(args):
    """Benchmark all models on a question."""
    models = list_models(speed=args.speed)
    
    print(f"{'Model':<25} {'Time':>6}  {'Answer':<20}")
    print("-" * 55)
    
    for alias in sorted(models):
        t0 = time.time()
        ans, raw = call_model(
            args.question, alias,
            system_prompt=args.system,
        )
        dt = time.time() - t0
        first_line = raw.strip().split('\n')[0][:60] if raw else "?"
        print(f"{alias:<25} {dt:5.1f}s  {ans:<20} {first_line}")


def cmd_models(args):
    """List available models."""
    for alias in sorted(MODELS.keys()):
        m = MODELS[alias]
        think = " 🧠" if m.get("thinking") else ""
        print(f"  {alias:<25} {m['speed']:<8} {m['family']:<10} {m['params']:<6}{think}")


def cmd_panels(args):
    """List available panels."""
    for name, aliases in PANELS.items():
        models_str = ", ".join(aliases)
        print(f"  {name:<12} [{len(aliases)} models] {models_str}")


def main():
    parser = argparse.ArgumentParser(
        prog="nim-ensemble",
        description="$0 test-time scaling with NVIDIA NIM free tier",
    )
    sub = parser.add_subparsers(dest="command")
    
    # scale (primary API)
    p_scale = sub.add_parser("scale", help="Scale inference to k models")
    p_scale.add_argument("question", help="Question to answer")
    p_scale.add_argument("-k", default="auto", help="Number of models: 1, 3, 5, or 'auto' (default: auto)")
    p_scale.add_argument("--answers", "-a", help="Comma-separated valid answers")
    p_scale.add_argument("--system", "-s", help="System prompt")
    p_scale.add_argument("--json", "-j", action="store_true")
    p_scale.add_argument("--verbose", "-v", action="store_true")
    p_scale.set_defaults(func=cmd_scale)
    
    # smart (cascade — alias for scale --k auto)
    p_smart = sub.add_parser("smart", help="Smart cascade (alias for scale -k auto)")
    p_smart.add_argument("question", help="Question to answer")
    p_smart.add_argument("--answers", "-a", help="Comma-separated valid answers")
    p_smart.add_argument("--type", "-t", help="Task type (code/compliance/reasoning/factual/nuance)")
    p_smart.add_argument("--system", "-s", help="System prompt")
    p_smart.add_argument("--threshold", type=float, default=0.85, help="Confidence threshold (default 0.85)")
    p_smart.add_argument("--flat", action="store_true", help="Skip cascade, use weighted panel vote")
    p_smart.add_argument("--json", "-j", action="store_true")
    p_smart.add_argument("--verbose", "-v", action="store_true")
    p_smart.set_defaults(func=cmd_smart)
    
    # classify
    p_classify = sub.add_parser("classify", help="Classify task type")
    p_classify.add_argument("question", help="Question to classify")
    p_classify.set_defaults(func=cmd_classify)
    
    # ask (flat ensemble)
    p_ask = sub.add_parser("ask", help="Flat ensemble vote")
    p_ask.add_argument("question", help="Question to vote on")
    p_ask.add_argument("--panel", "-p", default="general", help="Model panel")
    p_ask.add_argument("--answers", "-a", help="Comma-separated valid answers")
    p_ask.add_argument("--system", "-s", help="System prompt")
    p_ask.add_argument("--json", "-j", action="store_true")
    p_ask.add_argument("--verbose", "-v", action="store_true")
    p_ask.add_argument("--no-short-circuit", action="store_true")
    p_ask.set_defaults(func=cmd_ask)
    
    # bench
    p_bench = sub.add_parser("bench", help="Benchmark models")
    p_bench.add_argument("question", help="Question to benchmark")
    p_bench.add_argument("--system", "-s", help="System prompt")
    p_bench.add_argument("--speed", help="Filter: fast/medium/slow")
    p_bench.set_defaults(func=cmd_bench)
    
    # models
    p_models = sub.add_parser("models", help="List models")
    p_models.set_defaults(func=cmd_models)
    
    # panels
    p_panels = sub.add_parser("panels", help="List panels")
    p_panels.set_defaults(func=cmd_panels)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
