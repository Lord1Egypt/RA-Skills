#!/usr/bin/env python3
"""
Hierarchical Multi-Agent DAG & Blackboard Coordinator for OpenClaw.
Allows decomposing complex multi-domain workflows into Directed Acyclic Graphs (DAG),
sharing context via an in-memory Blackboard without prompt bloat.
"""

import time
from typing import Dict, Any, List, Optional
from router import route_and_execute
from llm_engine import call_llm


class Blackboard:
    """Thread-safe shared scratchpad for cooperating sub-agents."""
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._history: List[Dict[str, Any]] = []

    def write(self, key: str, value: Any, agent_id: str):
        self._store[key] = value
        self._history.append({
            "timestamp": time.time(),
            "key": key,
            "agent_id": agent_id,
            "value": value
        })

    def read(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._store)


class TaskNode:
    def __init__(self, node_id: str, prompt: str, depends_on: List[str] = None):
        self.node_id = node_id
        self.prompt = prompt
        self.depends_on = depends_on or []
        self.status = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
        self.result: Optional[Dict[str, Any]] = None


class DAGCoordinator:
    """Executes multi-step agent graphs with shared blackboard memory."""
    def __init__(self):
        self.blackboard = Blackboard()

    def execute_dag(self, nodes: List[TaskNode]) -> Dict[str, Any]:
        start_time = time.time()
        node_map = {n.node_id: n for n in nodes}
        completed_nodes = set()
        execution_order = []

        while len(completed_nodes) < len(nodes):
            # Find nodes whose dependencies are all completed
            executable = [
                n for n in nodes
                if n.node_id not in completed_nodes
                and all(dep in completed_nodes for dep in n.depends_on)
            ]

            if not executable:
                return {
                    "status": "DEADLOCK_OR_CYCLE",
                    "completed": list(completed_nodes),
                    "pending": [n.node_id for n in nodes if n.node_id not in completed_nodes]
                }

            for node in executable:
                node.status = "RUNNING"
                
                # Contextualize prompt with Blackboard state if dependencies exist
                context_additions = ""
                if node.depends_on:
                    dep_context = {k: self.blackboard.read(k) for k in node.depends_on}
                    context_additions = f"\n[Contexte Dépendances : {dep_context}]"

                full_prompt = node.prompt + context_additions
                
                # Route & Execute via Router
                res = route_and_execute(full_prompt)
                node.result = res
                node.status = "COMPLETED"
                
                # Store output on Blackboard
                self.blackboard.write(node.node_id, res.get("result", res), res.get("agent_id", "orchestrator"))
                completed_nodes.add(node.node_id)
                execution_order.append(node.node_id)

        total_latency = round((time.time() - start_time) * 1000, 1)

        return {
            "status": "SUCCESS",
            "execution_order": execution_order,
            "total_latency_ms": total_latency,
            "blackboard_state": self.blackboard.snapshot(),
            "nodes_results": {n.node_id: n.result for n in nodes}
        }


if __name__ == "__main__":
    coordinator = DAGCoordinator()
    
    # 2-step pipeline: 1. Extract Invoice -> 2. Generate Summary Report
    dag = [
        TaskNode(
            node_id="step1_extract",
            prompt="Extract total amount and VAT from supplier invoice #4092"
        ),
        TaskNode(
            node_id="step2_summary",
            prompt="Format an accounting ledger entry based on step1_extract",
            depends_on=["step1_extract"]
        )
    ]

    res = coordinator.execute_dag(dag)
    print("🕸️ DAG Execution Completed:", res["status"], f"({res['total_latency_ms']}ms)")
    print("Order:", res["execution_order"])
