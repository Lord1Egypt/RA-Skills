#!/usr/bin/env python3
"""learning_engine.py - Pattern learning for smart routing v0.5.0"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class LearningEngine:
    """Learn from task patterns to improve routing decisions."""

    def __init__(self, db_path="/a0/usr/projects/frugal_orchestrator/logs/patterns.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.patterns = self._load()

    def _load(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                return json.load(f)
        return {"tasks": [], "route_stats": defaultdict(lambda: {"count": 0, "success": 0, "tokens_saved": 0})}

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump({
                "tasks": self.patterns["tasks"][-1000:],
                "route_stats": dict(self.patterns["route_stats"])
            }, f, indent=2)

    def record_task(self, task_type, routed_to, success, tokens_saved=0):
        self.patterns["tasks"].append({
            "task": task_type,
            "routed_to": routed_to,
            "success": success,
            "tokens_saved": tokens_saved,
            "ts": datetime.now().isoformat()
        })

        stats = self.patterns["route_stats"][routed_to]
        stats["count"] += 1
        if success:
            stats["success"] += 1
        stats["tokens_saved"] += tokens_saved

        if len(self.patterns["tasks"]) % 10 == 0:
            self._save()

    def suggest_route(self, task_description):
        words = task_description.lower().split()
        best = None
        best_score = 0

        for task in self.patterns["tasks"][-100:]:
            task_words = set(task["task"].lower().split())
            score = len(set(words) & task_words)
            if task["success"]:
                score *= 2
            if score > best_score:
                best_score = score
                best = task

        return best["routed_to"] if best else None

    def get_insights(self):
        stats = dict(self.patterns["route_stats"])
        if not stats:
            return {"message": "No patterns learned yet"}

        total = sum(s["count"] for s in stats.values())
        success = sum(s["success"] for s in stats.values())
        tokens = sum(s["tokens_saved"] for s in stats.values())

        return {
            "total_tasks": total,
            "success_rate": round(success / total * 100, 1) if total else 0,
            "total_tokens_saved": tokens,
            "route_performance": stats
        }

if __name__ == "__main__":
    print("LearningEngine standalone test")
    le = LearningEngine()
    le.record_task("Sort CSV", "system", True, 150)
    le.record_task("Analyze trends", "ai", True, 500)
    print("Insights:", le.get_insights())
    print("Suggestion for 'Sort CSV':", le.suggest_route("Sort CSV"))
