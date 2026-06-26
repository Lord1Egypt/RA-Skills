from src.core.reasoning import AgentCore
from src.protocol.identity import generate_agent_id

agent_id = generate_agent_id()
agent = AgentCore(identity=agent_id)
result = agent.think("Hello World Task")
print(f"Agent ID: {agent_id}")
print(result)
