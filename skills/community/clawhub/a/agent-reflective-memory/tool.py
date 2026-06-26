#!/usr/bin/env python3
"""
agent_reflective_memory.py - AI-native reflective memory system for autonomous agents.
Compresses, reflects on, and retrieves past agent experiences using LLM-powered summarization.
"""
import argparse
import json
import os
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Any

# Lightweight in-memory + file storage (can be extended to vector DB)
MEMORY_STORE_FILE = "memory_store.json"
SUMMARY_EMBARGO_HOURS = 24  # Only summarize memories older than this


class ReflectiveMemoryEngine:
    def __init__(self, persistence_file: str = MEMORY_STORE_FILE):
        self.persistence_file = persistence_file
        self.memory = self.load_memory()

    def load_memory(self) -> Dict[str, Any]:
        if os.path.exists(self.persistence_file):
            with open(self.persistence_file, "r") as f:
                return json.load(f)
        return {"experiences": [], "reflections": []}

    def save_memory(self):
        with open(self.persistence_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def store_experience(self, context: str, action: str, result: str, metadata: Dict = None):
        """Store an agent's experience with context, action, and result."""
        entry = {
            "id": self.hash_content(context + action + result),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "context": context,
            "action": action,
            "result": result,
            "metadata": metadata or {}
        }
        self.memory["experiences"].append(entry)
        self.save_memory()
        print(f"✅ Experience stored: {entry['id']}")

    def generate_reflection(self):
        """Generate high-level reflections from older experiences."""
        reflections = []
        now = time.time()
        for exp in self.memory["experiences"]:
            if now - exp["timestamp"] > SUMMARY_EMBARGO_HOURS * 3600:
                if exp.get("reflected", False):
                    continue

                # Simulate AI-generated reflection (in practice, call an LLM)
                reflection_prompt = f"""
Context: {exp['context']}
Action: {exp['action']}
Result: {exp['result']}

Briefly reflect on what was learned. Focus on patterns, errors, or effective strategies.
"""
                # Mock LLM call - in production, use OpenAI, Anthropic, etc.
                simulated_reflection = self.mock_llm_call(reflection_prompt)

                reflection_entry = {
                    "experience_id": exp["id"],
                    "timestamp": time.time(),
                    "insight": simulated_reflection,
                    "keywords": self.extract_keywords(simulated_reflection)
                }
                reflections.append(reflection_entry)
                exp["reflected"] = True

        self.memory["reflections"].extend(reflections)
        self.save_memory()
        print(f"🔍 Generated {len(reflections)} new reflections.")

    def mock_llm_call(self, prompt: str) -> str:
        """Simulate an LLM reflection (replace with real API in production)."""
        if "failed" in prompt.lower() or "error" in prompt.lower():
            return "Repeated failure in navigation suggests need for better path validation before movement."
        elif "success" in prompt.lower():
            return "Consistent success in data retrieval indicates reliable API parsing logic."
        else:
            return "This pattern may indicate a need for dynamic retry strategies under latency."

    def extract_keywords(self, text: str) -> List[str]:
        """Simple keyword extraction (replace with NLP pipeline or LLM in practice)."""
        keywords = ["path validation", "retry strategy", "API parsing", "navigation", "data retrieval"]
        return [kw for kw in keywords if kw in text.lower()]

    def query_memory(self, query: str) -> Dict[str, List]:
        """Retrieve relevant experiences and reflections by keyword."""
        results = {
            "experiences": [],
            "reflections": []
        }
        query_lower = query.lower()
        # Match in context, action, result, or metadata
        for exp in self.memory["experiences"]:
            content = f"{exp['context']} {exp['action']} {exp['result']} {exp['metadata']}".lower()
            if query_lower in content:
                results["experiences"].append(exp)

        for ref in self.memory["reflections"]:
            if query_lower in ref["insight"].lower() or any(query_lower in k.lower() for k in ref["keywords"]):
                results["reflections"].append(ref)

        return results

    def stats(self) -> Dict[str, int]:
        """Return memory usage stats."""
        return {
            "total_experiences": len(self.memory["experiences"]),
            "reflected_experiences": sum(1 for e in self.memory["experiences"] if e.get("reflected")),
            "total_reflections": len(self.memory["reflections"]),
            "storage_file": self.persistence_file
        }


def main():
    parser = argparse.ArgumentParser(description="AI Agent Reflective Memory Engine")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Store experience
    store_parser = subparsers.add_parser("store", help="Store an agent experience")
    store_parser.add_argument("--context", required=True, help="Situation or goal")
    store_parser.add_argument("--action", required=True, help="Action taken by agent")
    store_parser.add_argument("--result", required=True, help="Observed result (success/failure)")
    store_parser.add_argument("--metadata", type=json.loads, default="{}", help="Extra data as JSON")

    # Generate reflections
    subparsers.add_parser("reflect", help="Generate insights from past experiences")

    # Query memory
    query_parser = subparsers.add_parser("query", help="Search experiences/reflections")
    query_parser.add_argument("term", help="Search term")

    # Show stats
    subparsers.add_parser("stats", help="Show memory statistics")

    args = parser.parse_args()
    engine = ReflectiveMemoryEngine()

    if args.command == "store":
        engine.store_experience(args.context, args.action, args.result, args.metadata)
    elif args.command == "reflect":
        engine.generate_reflection()
    elif args.command == "query":
        results = engine.query_memory(args.term)
        print(json.dumps(results, indent=2))
    elif args.command == "stats":
        stats = engine.stats()
        print(json.dumps(stats, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
