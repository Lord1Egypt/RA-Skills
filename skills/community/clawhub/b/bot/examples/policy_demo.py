from src.protocol.alignment import AgentAlignment
from src.tools.registry import ToolRegistry
from src.tools.policy_executor import PolicyExecutor

def local_sum(a, b):
    return a + b

def main():
    alignment = AgentAlignment(mode="strict")
    registry = ToolRegistry()
    executor = PolicyExecutor(allow_network=False)

    registry.register(
        "local_sum",
        local_sum,
        capabilities=["local_compute"],
        description="Add two numbers locally"
    )

    tool = registry.get("local_sum")
    alignment.verify_capabilities(tool["capabilities"])

    result = executor.execute(tool["func"], 2, 3)
    print("Policy demo result:", result)
    print("Registered tools:", registry.list_tools())

if __name__ == "__main__":
    main()
