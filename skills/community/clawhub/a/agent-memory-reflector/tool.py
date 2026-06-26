#!/usr/bin/env python3
"""
agent_memory_reflector.py - Lightweight memory reflection engine for AI agents.
Enables introspection of past actions, reasoning path analysis, and self-improvement suggestions.
"""
import argparse
import json
import os
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional

VERSION = "0.2.1"


class MemoryReflector:
    def __init__(self, memory_dir: str = ".agent_memory", window_size: int = 50):
        self.memory_dir = memory_dir
        self.window_size = window_size
        self.memory_log = os.path.join(memory_dir, "memory.jsonl")
        self.reflection_log = os.path.join(memory_dir, "reflections.jsonl")
        
        os.makedirs(memory_dir, exist_ok=True)

    def log_interaction(self, agent_id: str, prompt: str, response: str, metadata: Dict = None):
        """Log an agent's input/output for future reflection."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
            "prompt": prompt,
            "response": response,
            "metadata": metadata or {},
            "entry_hash": self._hash_entry(prompt, response)
        }
        with open(self.memory_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _hash_entry(self, prompt: str, response: str) -> str:
        """Compute SHA-256 hash of combined prompt and response."""
        return hashlib.sha256((prompt + response).encode("utf-8")).hexdigest()

    def _load_recent_memories(self) -> List[Dict]:
        """Load the most recent interactions from memory."""
        if not os.path.exists(self.memory_log):
            return []

        with open(self.memory_log, "r") as f:
            lines = f.readlines()

        entries = [json.loads(line) for line in lines]
        return sorted(entries, key=lambda x: x["timestamp"], reverse=True)[:self.window_size]

    def detect_patterns(self) -> Dict:
        """Detect common patterns such as repetition, fallback usage, or high uncertainty."""
        memories = self._load_recent_memories()
        patterns = {
            "repeated_queries": [],
            "high_uncertainty_flags": [],
            "self_corrections": 0,
            "loop_detected": False
        }

        seen_hashes = set()
        for mem in memories:
            h = mem["entry_hash"]
            if h in seen_hashes:
                patterns["repeated_queries"].append(mem["prompt"][:120])
            seen_hashes.add(h)

            # Simple heuristic for uncertainty
            if any(phrase in mem["response"].lower() for phrase in ["i don't know", "unsure", "might be", "could be"]):
                patterns["high_uncertainty_flags"].append(mem["prompt"])

            # Detect self-correction in metadata
            if mem["metadata"].get("corrected_after") or mem["metadata"].get("self_edit"):
                patterns["self_corrections"] += 1

        if len(patterns["repeated_queries"]) > 5:
            patterns["loop_detected"] = True

        return patterns

    def generate_reflection_report(self) -> Dict:
        """Generate a reflection report with improvement suggestions."""
        patterns = self.detect_patterns()
        suggestions = []

        if patterns["loop_detected"]:
            suggestions.append("Agent appears stuck in reasoning loop. Consider adding state-tracking or forced exploration mode.")
        if len(patterns["high_uncertainty_flags"]) > 3:
            suggestions.append("Frequent uncertainty detected. Improve context injection or enable external retrieval.")
        if patterns["self_corrections"] > 5:
            suggestions.append("High self-correction rate. Evaluate if agent is over-editing — consider confidence thresholds.")

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "analysis_window": self.window_size,
            "detected_patterns": patterns,
            "suggestions": suggestions
        }

        with open(self.reflection_log, "a") as f:
            f.write(json.dumps(report) + "\n")

        return report


def main():
    parser = argparse.ArgumentParser(description="Agent Memory Reflector - Reflect on AI agent decisions and improve performance.")
    parser.add_argument("--agent", type=str, required=True, help="Agent ID or name")
    parser.add_argument("--prompt", type=str, help="The prompt given to the agent")
    parser.add_argument("--response", type=str, help="The agent's response")
    parser.add_argument("--meta", type=str, help='Metadata as JSON string, e.g. {"task":"planning", "confidence":0.7}')
    parser.add_argument("--reflect", action="store_true", help="Run reflection analysis on recent memories")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    args = parser.parse_args()

    reflector = MemoryReflector()

    if args.prompt and args.response:
        metadata = {}
        if args.meta:
            try:
                metadata = json.loads(args.meta)
            except json.JSONDecodeError as e:
                print(f"Error parsing metadata JSON: {e}")
                return 1
        reflector.log_interaction(args.agent, args.prompt, args.response, metadata)
        print("Interaction logged.")

    if args.reflect:
        report = reflector.generate_reflection_report()
        print("\n--- Reflection Report ---")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Patterns Found: {len(report['suggestions'])} issue(s) detected\n")
        for i, suggestion in enumerate(report["suggestions"], 1):
            print(f"{i}. {suggestion}")
        print("\nAnalysis complete. Check `.agent_memory/reflections.jsonl` for full details.")

    if not args.prompt and not args.reflect:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
