# ACC Error Memory ⚡

> Error pattern tracking for AI agents — the "something's off" detector

Part of the [AI Brain series](https://clawhub.ai/skills?tag=ai-brain) — giving AI agents human-like cognitive components.

## What It Does

Track errors and learn from mistakes:

- **Detects** when users correct or express frustration
- **Logs** error patterns with context and mitigations
- **Escalates** recurring patterns (normal → warning → critical)
- **Resolves** patterns that haven't recurred in 30+ days

## Quick Install

```bash
clawhub install acc-error-memory
cd ~/.openclaw/workspace/skills/acc-error-memory
./install.sh --with-cron
```

## How It Works

1. **Preprocessing** — Extracts user+assistant exchanges from transcripts
2. **Analysis** — LLM detects corrections, frustration, confusion
3. **Logging** — Errors logged with pattern names
4. **Tracking** — Patterns escalate with repetition

```
Exchange: "The latest Python is 3.9" → "Actually it's 3.12"
         ↓
Pattern: factual_error (now at 2x = warning)
         ↓
Mitigation: "Always verify versions with web search"
```

## At Session Start

Load ACC state to see what to watch for:

```bash
./scripts/load-state.sh

# ⚡ ACC State:
# 🔴 factual_error: 3x (critical) — verify before stating facts
# ⚠️ tone_mismatch: 2x (warning) — match user's emotional state
# ✅ missed_context: resolved 32 days ago
```

## Related Skills

| Skill | Function |
|-------|----------|
| [hippocampus](https://clawhub.ai/skills/hippocampus) | Memory with decay/reinforcement |
| [amygdala-memory](https://clawhub.ai/skills/amygdala-memory) | Emotional state tracking |
| [vta-memory](https://clawhub.ai/skills/vta-memory) | Motivation/reward system |

## License

MIT
