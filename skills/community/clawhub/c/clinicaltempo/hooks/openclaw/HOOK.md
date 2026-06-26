---
name: clinicaltempo-clawhub
description: "Injects Clinical Tempo / ClawHub context reminder during agent bootstrap (llm-full.txt, CLAWHUB.md, API smoke)."
metadata:
  openclaw:
    emoji: "🏥"
    events:
      - agent:bootstrap
---

# Clinical Tempo · ClawHub context hook

Injects a short **virtual bootstrap file** so agents remember where full repo context and tribal debugging live.

## What it does

- Fires on **`agent:bootstrap`** (before workspace files are injected).
- Pushes **`CLINICAL_TEMPO_CONTEXT_REMINDER.md`** into `bootstrapFiles` (virtual).
- Skips **sub-agent** sessions (same pattern as self-improving-agent) to avoid noisy duplicates.

## Enable

```bash
# From the skill directory, or from a copy of this repo’s .cursor/skills/clawhub/
cp -r hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub

openclaw hooks enable clinicaltempo-clawhub
```

Disable:

```bash
openclaw hooks disable clinicaltempo-clawhub
```

## Configuration

None. No network calls; no secrets.

## See also

- Skill: `../../SKILL.md`
- OpenClaw alignment: `../../references/openclaw-clinical-tempo.md`
