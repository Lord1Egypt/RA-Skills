---
name: dancetempo-clawhub
description: "Injects DanceTempo / ClawHub context reminder during agent bootstrap (llm-full.txt, CLAWHUB.md, API smoke)."
metadata:
  openclaw:
    emoji: "🎵"
    events:
      - agent:bootstrap
---

# DanceTempo · ClawHub context hook

Injects a short **virtual bootstrap file** so agents remember where full repo context and tribal debugging live.

## What it does

- Fires on **`agent:bootstrap`** (before workspace files are injected).
- Pushes **`DANCETEMPO_CONTEXT_REMINDER.md`** into `bootstrapFiles` (virtual).
- Skips **sub-agent** sessions (same pattern as self-improving-agent) to avoid noisy duplicates.

## Enable

```bash
# From the skill directory, or from a copy of this repo’s .cursor/skills/clawhub/
cp -r hooks/openclaw ~/.openclaw/hooks/dancetempo-clawhub

openclaw hooks enable dancetempo-clawhub
```

Disable:

```bash
openclaw hooks disable dancetempo-clawhub
```

## Configuration

None. No network calls; no secrets.

## See also

- Skill: `../../SKILL.md`
- OpenClaw alignment: `../../references/openclaw-dancetempo.md`
