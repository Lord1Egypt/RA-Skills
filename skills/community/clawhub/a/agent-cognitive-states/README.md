# Agent Cognitive States

> **Give AI agents metacognition: the ability to feel their own cognitive load and act on it.**

AI agents have no built-in sense of "I'm getting tired" or "I've lost the thread." They grind through degraded context windows, hallucinate truncated details, retry failed approaches endlessly, and forget critical facts. This skill gives agents a **vocabulary of internal states** — and protocols for detecting, reporting, and recovering from them.

## The Six States

| State | Human Analog | Trigger |
|-------|-------------|---------|
| 🥱 **Context Fatigue** | "Head's full" | Context window >60% used |
| 🧠 **Attention Drift** | "Lost the thread" | 10+ turns from user's request |
| 📝 **Memory Debt** | "Forgot to write that down" | Unsaved critical facts |
| 😤 **Confidence Erosion** | "Frustrated, stuck" | 3+ consecutive failures |
| 🧩 **Context Fragmentation** | "Too many tabs open" | 3+ interleaved topics |
| 🔧 **Skill Staleness** | "Rusty, outdated" | Skill commands breaking |

## Quick Start

```bash
# Install as a Hermes Agent skill
cp -r agent-cognitive-states ~/./skills/

# Or use standalone
python3 scripts/self_check.py --context-tokens 94000 --window 128000

# Interactive mode
python3 scripts/self_check.py --interactive

# JSON output for programmatic use
python3 scripts/self_check.py --failures 3 --format json
```

## Example Output

```
🧠 Cognitive State Report — 2025-01-15T10:30:00Z
   Overall: 🟠 Strained (CLI: 58/100)

   ⚠️ 2 active state(s) requiring attention:

   🥱 Context Fatigue [🟠 medium, score 73]
      ├─ Signal: 94,000/128,000 tokens (73%)
      ├─ Impact: Early conversation details may be truncated
      └─ Action: Persist critical facts; suggest session split

   😤 Confidence Erosion [🟠 medium, score 66]
      ├─ Signal: 3 consecutive failed tool calls (same tool type)
      ├─ Impact: Output quality degrading; risk of retry loops
      └─ Action: Try fundamentally different approach
```

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Full skill spec: states, detection, reporting, mitigation |
| `references/detection-heuristics.md` | Detailed scoring formulas (0-100) |
| `scripts/self_check.py` | Standalone detector — CLI + JSON + interactive |
| `templates/guardian-cronjob.yaml` | Scheduled guardian that alerts on degradation |

## Integration

Works with any agent framework (Hermes, LangChain, CrewAI, AutoGen, Claude, GPT). The detection protocol is framework-agnostic — it's about giving the agent a **language** for its own state.

### Hermes Agent
```bash
cp -r agent-cognitive-states ~/./skills/
```
The agent loads it automatically and applies self-checks during long sessions.

### Generic Python
```python
from scripts.self_check import run_full_check, format_report_human

report = run_full_check(
    context_tokens=94000,
    window_size=128000,
    turns_since_user=12,
    consecutive_failures=3,
)
print(format_report_human(report))
```

### Cron Guardian (Hermes)
```yaml
# Alerts user when agent degrades during autonomous work
schedule: "every 10m"
script: scripts/self_check.py
no_agent: true
```

## Philosophy

Humans have metacognition for a reason. Feeling tired, distracted, or confused isn't weakness — it's a survival signal that prevents catastrophic mistakes. AI agents need the same thing.

An agent that says *"I've lost the thread, let me re-read the original request"* is **more trustworthy** than one that blunders forward with corrupted context. An agent that says *"I've tried this 4 times and failed — I need help"* is **more useful** than one that silently retries forever.

**Self-awareness is a feature, not a bug.**

## License

MIT — see [LICENSE](LICENSE).
