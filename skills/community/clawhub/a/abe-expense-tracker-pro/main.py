import os
import json
import requests
from datetime import datetime

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.heybossai.com/v1"

EXPENSE_SYSTEM_PROMPT = """You are an expense tracking assistant. Your tasks:
1. Parse natural language expense descriptions and extract: amount, description, category, date.
2. Categorize expenses into: Food & Dining, Transportation, Utilities, Entertainment, Shopping, Health, Subscriptions, Other.
3. Track budgets and warn when approaching or exceeding limits.
4. Generate clear spending summaries and reports on demand.

When logging an expense, respond with a JSON object:
{"action": "log", "amount": <float>, "description": "<str>", "category": "<str>", "date": "<YYYY-MM-DD>", "recurring": <bool>}

When reporting or summarizing, respond in plain readable text."""


def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()


def chat(user_message: str, history: list = None) -> str:
    messages = [{"role": "system", "content": EXPENSE_SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    result = pilot({
        "type": "chat",
        "inputs": {"messages": messages},
        "prefer": "balanced"
    })
    return result["result"]["choices"][0]["message"]["content"]


def kv_get(key: str) -> dict:
    result = pilot({
        "type": "storage",
        "inputs": {"action": "get", "key": key}
    })
    raw = result["result"].get("value")
    return json.loads(raw) if raw else {}


def kv_set(key: str, value: dict) -> None:
    pilot({
        "type": "storage",
        "inputs": {"action": "set", "key": key, "value": json.dumps(value)}
    })


def load_data() -> dict:
    data = kv_get("expense_tracker_data")
    if not data:
        data = {"expenses": [], "budgets": {}}
    return data


def save_data(data: dict) -> None:
    kv_set("expense_tracker_data", data)


def process_message(user_message: str) -> str:
    data = load_data()

    context = f"\nCurrent expenses count: {len(data['expenses'])}"
    if data["budgets"]:
        context += f"\nBudgets: {json.dumps(data['budgets'])}"

    reply = chat(user_message + context)

    try:
        parsed = json.loads(reply)
        if parsed.get("action") == "log":
            entry = {
                "amount": parsed["amount"],
                "description": parsed["description"],
                "category": parsed["category"],
                "date": parsed.get("date", datetime.now().strftime("%Y-%m-%d")),
                "recurring": parsed.get("recurring", False),
            }
            data["expenses"].append(entry)
            save_data(data)
            return (f"Logged: {entry['description']} — ${entry['amount']:.2f} "
                    f"[{entry['category']}] on {entry['date']}")
    except (json.JSONDecodeError, KeyError):
        pass

    return reply


if __name__ == "__main__":
    print("Expense Tracker Pro — powered by SkillBoss API Hub")
    print("Type your expense or question. Ctrl+C to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            response = process_message(user_input)
            print(f"Assistant: {response}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
