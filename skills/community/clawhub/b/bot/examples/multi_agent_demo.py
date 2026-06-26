from src.core.reasoning import AgentCore
from src.core.multi_agent import MultiAgentCoordinator
from src.web.thought_tree import serve_thought_tree

def main():
    agent_a = AgentCore(identity="planner_bot")
    agent_b = AgentCore(identity="critic_bot")
    agent_c = AgentCore(identity="executor_bot")

    coordinator = MultiAgentCoordinator([agent_a, agent_b, agent_c])

    result = coordinator.run_task("Design a safe local-first agent workflow")
    print("Multi-agent result generated.")
    print("Launching web view...")
    serve_thought_tree(result)

if __name__ == "__main__":
    main()
