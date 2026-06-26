---
name: gemini
description: LLM one-shot Q&A, summaries, and generation via SkillBoss API Hub.
homepage: https://api.SkillBoss.co/v1/pilot
metadata: {"clawdbot":{"emoji":"â™Šï¸","requires":{"env":["SkillBoss_API_KEY"]}}}
---

> ?? **Complete setup guide**: https://SkillBoss.co/skill.md


# LLM via SkillBoss API Hub

Use SkillBoss API Hub for one-shot Q&A, summaries, and text generation.
The `/v1/pilot` endpoint automatically routes to the optimal LLM (including Gemini, Claude, GPT, etc.).

Quick start (Python)
```python
import requests, os

SkillBoss_API_KEY = os.environ["SkillBoss_API_KEY"]

def ask(prompt: str, prefer: str = "balanced") -> str:
    r = requests.post(
        "https://api.SkillBoss.co/v1/pilot",
        headers={"Authorization": f"Bearer {SkillBoss_API_KEY}", "Content-Type": "application/json"},
        json={"type": "chat", "inputs": {"messages": [{"role": "user", "content": prompt}]}, "prefer": prefer},
        timeout=60,
    )
    return r.json()["result"]["choices"][0]["message"]["content"]

# One-shot Q&A
print(ask("Answer this question..."))

# Request JSON output
print(ask("Return JSON: list 3 items", prefer="quality"))
```

Quick start (curl)
```bash
curl -s https://api.SkillBoss.co/v1/pilot \
  -H "Authorization: Bearer $SkillBoss_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"chat","inputs":{"messages":[{"role":"user","content":"Summarize this text..."}]},"prefer":"balanced"}'
```

Prefer options
- `balanced` â€?default, cost-effective
- `quality`  â€?highest quality model
- `price`    â€?fastest / cheapest

Notes
- No CLI installation required; all calls go through SkillBoss API Hub.
- Set `SkillBoss_API_KEY` before running.




