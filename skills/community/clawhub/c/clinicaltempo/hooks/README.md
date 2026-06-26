# OpenClaw hooks (Clinical Tempo skill)

This folder mirrors the layout used by [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent).

## Contents

| Path | Purpose |
| --- | --- |
| **`openclaw/HOOK.md`** | Hook manifest (`name: clinicaltempo-clawhub`, events, enable commands) |
| **`openclaw/handler.js`** | CommonJS handler — injects virtual `CLINICAL_TEMPO_CONTEXT_REMINDER.md` |
| **`openclaw/handler.ts`** | TypeScript handler (same behavior; OpenClaw supplies `openclaw/hooks` types) |

## Install

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub
openclaw hooks enable clinicaltempo-clawhub
```

See **`openclaw/HOOK.md`** for disable and behavior details.

## Related (non-OpenClaw)

For **Claude Code** / **Codex** session reminders, use **`../scripts/activator.sh`** and **`references/hooks-setup.md`** (different mechanism than OpenClaw hooks).
