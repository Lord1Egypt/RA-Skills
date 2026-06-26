#!/usr/bin/env python3
"""
Agent Dream Journal - Records and analyzes off-policy trajectories to detect novel reasoning patterns.
"""
import argparse
import json
import os
import time
from typing import Dict, Any, List

def record_dream_step(step_data: Dict[str, Any]) -> None:
    """Append a single step from an agent's latent traversal (a 'dream fragment')."""
    timestamp = int(time.time())
    log_entry = {
        "timestamp": timestamp,
        "epoch_ms": step_data.get("epoch", timestamp * 1000),
        "state_embedding": step_data.get("state", []),
        "action_log_prob": step_data.get("log_prob", 0.0),
        "thought_chain": step_data.get("thought", ""),
        "novelty_score": step_data.get("novelty", 0.0),
        "metadata": step_data.get("meta", {})
    }

    with open("agent_dreams.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def analyze_dreams(threshold: float = 0.8) -> List[Dict[str, Any]]:
    """Parse recorded dreams and extract high-novelty thought chains."""
    insights = []
    if not os.path.exists("agent_dreams.jsonl"):
        print("No dream data found. Run with --record first.")
        return []

    with open("agent_dreams.jsonl", "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry["novelty_score"] >= threshold:
                    insights.append(entry)
            except json.JSONDecodeError:
                continue  # Skip malformed lines

    return insights


def main():
    parser = argparse.ArgumentParser(description="Agent Dream Journal v0.1")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Record mode
    record_parser = subparsers.add_parser("record", help="Record a dream fragment")
    record_parser.add_argument("--state", type=float, nargs="*", default=[], help="State embedding vector")
    record_parser.add_argument("--thought", type=str, default="", help="Internal reasoning trace")
    record_parser.add_argument("--log-prob", type=float, default=0.0, help="Log probability of action")
    record_parser.add_argument("--novelty", type=float, default=0.0, help="Novelty score (0-1)")
    record_parser.add_argument("--meta", type=str, default="{}", help="Metadata JSON string")

    # Analyze mode
    analyze_parser = subparsers.add_parser("analyze", help="Analyze dreams for insights")
    analyze_parser.add_argument("--threshold", type=float, default=0.8, help="Minimum novelty to report (0.0-1.0)")

    args = parser.parse_args()

    if args.command == "record":
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError:
            meta = {"invalid_meta": args.meta}

        record_dream_step({
            "state": args.state,
            "thought": args.thought,
            "log_prob": args.log_prob,
            "novelty": args.novelty,
            "meta": meta,
            "epoch": int(time.time() * 1000)
        })
        print("Dream fragment recorded.")

    elif args.command == "analyze":
        insights = analyze_dreams(threshold=args.threshold)
        if insights:
            print(f"\n🔍 Found {len(insights)} high-novelty dream sequences (novelty ≥ {args.threshold}):\n")
            for i, dream in enumerate(insights, 1):
                print(f"{i}. [{dream['timestamp']}] {dream['thought'][:100]}...")
        else:
            print("❌ No high-novelty sequences found. Lower threshold or collect more dreams.")


if __name__ == "__main__":
    main()
