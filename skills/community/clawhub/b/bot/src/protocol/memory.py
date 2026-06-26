import json
import os

MEMORY_PATH = os.environ.get("BOT_MEMORY_DIR", os.path.abspath(".bot_memory"))
os.makedirs(MEMORY_PATH, exist_ok=True)

def save_memory(agent_id: str, data: dict):
    path = os.path.join(MEMORY_PATH, f"{agent_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_memory(agent_id: str):
    path = os.path.join(MEMORY_PATH, f"{agent_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
