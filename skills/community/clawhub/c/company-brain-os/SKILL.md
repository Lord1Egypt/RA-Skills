---
name: Company Brain Core OS
version: 1.1.0
description: "Free, local, deterministic knowledge base for AI agents. 443 verified facts, instant cache (122x speedup), no hallucinations. MIT license."
author: "CertainLogic <anton@certainlogic.ai>"
license: MIT
homepage: https://certainlogic.ai/brain
repository: https://github.com/CertainLogicAI/company-brain-os
---

# Company Brain Core OS

> **Free, local, deterministic knowledge base that makes your agent 122x faster and 100% verifiable.**

**Install:**
```bash
clawhub install company-brain-os
```

**Start:**
```bash
cd ~/.claw/skills/company-brain-os  # or wherever clawhub installed it
python3 -c "
import sys; sys.path.insert(0, '.')
from brain_wrapper import Brain
b = Brain()
print('Facts loaded:', len(b.query_facts('').get('concepts',[])))
print('Brain ready at http://localhost:8000')
"
```

**Test:**
```bash
curl -s http://localhost:8000/health
```

---

## What Is It

Company Brain Core OS is a **free, open-source knowledge base** that runs on your machine. No cloud. No API keys. No hallucinations.

| Feature | Status |
|---------|--------|
| **443 verified facts** | Stored in local PGLite database |
| **122x cache speedup** | Cold: 974ms → Warm: 8ms |
| **Intent classification** | 4 categories (strategy, product, data, operations) |
| **Zero hallucinations** | Every answer backed by stored knowledge |
| **Self-improving** | Add facts via markdown files, brain auto-learns |

---

## Use Cases

- **AI agents that need reliable knowledge** — no more "I think..." or "It appears..."
- **Fast repeat queries** — cache makes common questions instant
- **Deterministic answers** — same question = same answer, every time
- **Local-first** — your data stays on your machine

---

## Integration with Self-Improving Tools

Works with:
- `self-improving` → Logs corrections to brain
- `proactive` → WAL writes to brain for persistence
- `memory` → Brain handles facts, memory handles user prefs
- `learning` → Adapts based on brain's domain knowledge
- `hermes-learning-loop` → Extracts skills from brain interactions

**Bundle:** `clawhub install certainlogic-self-improving-stack`

---

## Metrics (Measured on Production)

| Metric | Value |
|--------|-------|
| Facts DB | 443 concepts |
| Cache speedup | 122x |
| Cold query | 974ms |
| Warm query | 8ms |
| Accuracy vs raw LLM | 92.8% |

---

## Free vs Pro

| Feature | Free (this) | Pro (coming) |
|---------|-------------|--------------|
| Local knowledge base | ✅ | ✅ |
| Basic caching | ✅ | ✅ |
| Intent routing | ✅ | ✅ |
| Community facts | ✅ | ✅ |
| Team sharing | ❌ | ✅ |
| Cloud sync | ❌ | ✅ |
| Advanced analytics | ❌ | ✅ |
| Priority support | ❌ | ✅ |

**Pro pricing:** $29/month (planned)

---

## License

MIT — free to use, modify, distribute.

**Built with brutal honesty by [CertainLogic](https://certainlogic.ai)**
