#!/usr/bin/env python3
"""a2a_adapter.py - FastA2A mesh integration for Frugal Orchestrator v0.5.0"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

class A2AAdapter:
    """Connect orchestrator to FastA2A agent mesh."""

    def __init__(self, cache_dir="/a0/usr/projects/frugal_orchestrator/cache/a2a"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.agents = self._load_agent_registry()
        self.cache = {}

    def _load_agent_registry(self):
        registry_path = self.cache_dir / "agent_registry.json"
        if registry_path.exists():
            with open(registry_path) as f:
                return json.load(f)
        return {
            "researcher": {"url": "internal://researcher", "capabilities": ["research", "analysis"], "cost": 1.0},
            "developer": {"url": "internal://developer", "capabilities": ["code", "debug"], "cost": 1.2},
            "sysadmin": {"url": "internal://sysadmin", "capabilities": ["infrastructure", "docker"], "cost": 0.8}
        }

    def discover_agents(self, capability=None):
        if capability:
            return {k: v for k, v in self.agents.items() if capability in v["capabilities"]}
        return self.agents

    def route_intelligently(self, task_description):
        words = task_description.lower().split()
        scores = {}
        for agent_id, info in self.agents.items():
            score = sum(1 for cap in info["capabilities"] for word in words if cap in word)
            if score > 0:
                scores[agent_id] = score
        if scores:
            return max(scores, key=scores.get)
        return "developer"

    def cache_result(self, task_hash, result):
        self.cache[task_hash] = {"content": result, "ts": datetime.now().isoformat()}

    def get_cached(self, task_hash):
        return self.cache.get(task_hash)

if __name__ == "__main__":
    adapter = A2AAdapter()
    print("Agents:", list(adapter.discover_agents().keys()))
    print("Route 'Fix python bug':", adapter.route_intelligently("Fix python bug"))
