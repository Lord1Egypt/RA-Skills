import uuid

def generate_agent_id() -> str:
    return f"bot_{uuid.uuid4().hex[:8]}"
