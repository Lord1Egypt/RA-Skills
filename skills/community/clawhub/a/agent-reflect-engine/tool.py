#!/usr/bin/env python3
"""
agent_reflect_engine.py - AI Agent Self-Reflection & Optimization Engine
Analyzes agent decision logs to detect logical inconsistencies, hallucinations, and suboptimal reasoning patterns.
Outputs patch suggestions to improve future reasoning.
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict, Any

def load_logs(filepath: str) -> List[Dict[str, Any]]:
    """Load JSONL or JSON log file containing agent interaction traces."""
    logs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    logs.append(json.loads(line))
    except Exception as e:
        print(f"Error loading logs: {e}", file=sys.stderr)
        sys.exit(1)
    return logs

def detect_repetition(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect repeated actions or thoughts indicating stuck reasoning loops."""
    issues = []
    for i in range(1, len(logs)):
        prev, curr = logs[i-1], logs[i]
        if prev.get("action") == curr.get("action") and prev.get("thought") == curr.get("thought"):
            issues.append({
                "type": "repetition_loop",
                "timestamp": curr.get("timestamp", datetime.now().isoformat()),
                "context": f"Repeated action/thought at step {i}: {curr.get('action')}"
            })
    return issues

def detect_hallucination(logs: List[Dict[str, Any]], knowledge_base: List[str] = None) -> List[Dict[str, Any]]:
    """Detect claims unsupported by prior observation (basic hallucination detection)."""
    if not knowledge_base:
        knowledge_base = []
    issues = []
    observations = set()
    for entry in logs:
        if "observation" in entry:
            observations.add(entry["observation"].lower())
    for entry in logs:
        if "thought" in entry:
            thought = entry["thought"].lower()
            # Simple heuristic: if a 'fact' in thought wasn't in observation
            if "i know that" in thought or "recall that" in thought:
                known_facts = [fact for fact in knowledge_base if fact.lower() in thought]
                if not known_facts and not any(obs in thought for obs in observations):
                    issues.append({
                        "type": "potential_hallucination",
                        "timestamp": entry.get("timestamp", datetime.now().isoformat()),
                        "suspicious_claim": thought
                    })
    return issues

def detect_suboptimal_routing(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detect inefficient task routing (e.g., excessive tool calls before success)."""
    issues = []
    tool_calls = 0
    last_goal = None
    for entry in logs:
        if "goal" in entry:
            if last_goal and tool_calls > 5:
                issues.append({
                    "type": "inefficient_execution",
                    "goal": last_goal,
                    "tool_calls_before_completion": tool_calls
                })
            last_goal = entry["goal"]
            tool_calls = 0
        if entry.get("action", "").startswith("call_tool"):
            tool_calls += 1
    return issues

def generate_patch_suggestions(issues: List[Dict[str, Any]]) -> List[str]:
    """Generate actionable patches based on detected issues."""
    suggestions = set()
    for issue in issues:
        if issue["type"] == "repetition_loop":
            suggestions.add("Add early exit condition for repeated thought-action sequences.")
        elif issue["type"] == "potential_hallucination":
            suggestions.add("Validate generated knowledge against observation log before use.")
        elif issue["type"] == "inefficient_execution":
            suggestions.add("Implement dynamic tool call budget per task to prevent overuse.")
    return list(suggestions)

def main():
    parser = argparse.ArgumentParser(description="AI Agent Self-Reflection Engine")
    parser.add_argument("log_file", help="Path to agent log file (JSONL or JSON)")
    parser.add_argument("--knowledge", help="Path to trusted knowledge base (JSON list)", default=None)
    parser.add_argument("--output", help="Output file for report (default: stdout)", default=None)

    args = parser.parse_args()

    logs = load_logs(args.log_file)
    if not logs:
        print("No log data to analyze.", file=sys.stderr)
        sys.exit(1)

    knowledge = []
    if args.knowledge:
        try:
            with open(args.knowledge, 'r') as f:
                knowledge = json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}", file=sys.stderr)

    issues = []
    issues += detect_repetition(logs)
    issues += detect_hallucination(logs, knowledge)
    issues += detect_suboptimal_routing(logs)

    patches = generate_patch_suggestions(issues)

    report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "total_entries": len(logs),
        "detected_issues": issues,
        "patch_suggestions": patches
    }

    output_stream = open(args.output, 'w') if args.output else sys.stdout
    json.dump(report, output_stream, indent=2)
    if args.output:
        output_stream.close()

    if patches:
        print(f"\n✅ Found {len(issues)} issues. Suggested patches:", file=sys.stderr)
        for patch in patches:
            print(f"   - {patch}", file=sys.stderr)
    else:
        print(f"\n✅ Clean bill of health: No critical issues found.", file=sys.stderr)

if __name__ == "__main__":
    main()
