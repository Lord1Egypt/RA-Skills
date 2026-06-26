# OpenClaw hooks (DanceTempo skill)

This folder mirrors the layout used by [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent).

## Contents

| Path | Purpose |
| --- | --- |
| **`openclaw/HOOK.md`** | Hook manifest (`name: dancetempo-clawhub`, events, enable commands) |
| **`openclaw/handler.js`** | CommonJS handler — injects virtual `DANCETEMPO_CONTEXT_REMINDER.md` |
| **`openclaw/handler.ts`** | TypeScript handler (same behavior; OpenClaw supplies `openclaw/hooks` types) |

## Install

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/dancetempo-clawhub
openclaw hooks enable dancetempo-clawhub
```

See **`openclaw/HOOK.md`** for disable and behavior details.
