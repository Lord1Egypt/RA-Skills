from typing import List, Dict, Any

class MultiAgentCoordinator:
    def __init__(self, agents: List[Any]):
        self.agents = agents

    def run_task(self, prompt: str) -> Dict[str, Any]:
        steps = []
        agent_results = []

        for idx, agent in enumerate(self.agents, start=1):
            result = agent.think(f"[Agent {idx}] {prompt}")
            agent_results.append({
                "agent": agent.identity,
                "result": result
            })
            steps.append({
                "id": f"agent_{idx}",
                "label": agent.identity,
                "thoughts": result.get("thought_process", []),
                "confidence": result.get("confidence_score", 0.0),
                "children": []
            })

        tree = {
            "id": "root",
            "label": "Multi-Agent Task",
            "prompt": prompt,
            "children": steps
        }

        return {
            "prompt": prompt,
            "agents": agent_results,
            "thought_tree": tree
        }
