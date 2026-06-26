import argparse

from src.core.reasoning import AgentCore
from src.core.multi_agent import MultiAgentCoordinator
from src.web.thought_tree import serve_thought_tree

def main():
    parser = argparse.ArgumentParser(description="Run bot in single-agent or multi-agent mode")
    parser.add_argument("--mode", choices=["single", "multi"], default="multi")
    parser.add_argument("--prompt", default="Design a safe local-first agent workflow")
    parser.add_argument("--roles", default="planner_bot,critic_bot,executor_bot")
    args = parser.parse_args()

    if args.mode == "single":
        agent = AgentCore(identity="solo_bot")
        result = {
            "prompt": args.prompt,
            "agents": [
                {
                    "agent": agent.identity,
                    "result": agent.think(args.prompt)
                }
            ],
            "thought_tree": {
                "id": "root",
                "label": "Single-Agent Task",
                "prompt": args.prompt,
                "children": [
                    {
                        "id": "agent_1",
                        "label": agent.identity,
                        "thoughts": agent.think(args.prompt).get("thought_process", []),
                        "confidence": agent.think(args.prompt).get("confidence_score", 0.0),
                        "children": []
                    }
                ]
            }
        }
    else:
        roles = [r.strip() for r in args.roles.split(",") if r.strip()]
        agents = [AgentCore(identity=role) for role in roles]
        coordinator = MultiAgentCoordinator(agents)
        result = coordinator.run_task(args.prompt)

    print("BOT run generated.")
    print("Launching web view...")
    serve_thought_tree(result)

if __name__ == "__main__":
    main()
