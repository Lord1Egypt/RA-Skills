# Pre-Action Check — Hook Layer Map

> **Read this if you arrived here from `openclaw plugins install` or `openclaw hooks install` and got an error.**

There is no executable hook file at this path because this sub-skill is intentionally **prompt-layer only** — a reasoning routine for the agent to run inside its own context window. The real `before_tool_call` enforcement hook lives in the companion plugin package.

## What you probably want

| You were trying to … | What you actually want |
|----------------------|------------------------|
| Install the five-question gate as a runtime hook | `openclaw plugins install clawhub:ovrsr/openclaw-fpp-plugin` |
| Install the constitutional skill so the agent reads it | `openclaw skills install freedom-preserving-protocol` |
| See the hook show up in `openclaw hooks list` | After installing the plugin: `openclaw plugins list \| grep openclaw-fpp-plugin` (note: plugin hooks register through the plugin SDK, not via standalone HOOK.md scripts) |

## Why this is split into two artifacts

OpenClaw distinguishes between:

- **Skills** — markdown packages the agent reads at prompt time. They cannot register hooks. They live at `~/.openclaw/skills/<id>/`.
- **Plugins** — TypeScript packages that register dispatcher-level hooks via `api.on("before_tool_call", ...)`. They live at `~/.openclaw/extensions/<id>/`.
- **Internal `HOOK.md` scripts** — small operator-installed scripts for command events like `/new`, `/reset`, `agent:bootstrap`, `gateway:startup`. **Not** for `before_tool_call` (which is a plugin-API hook, not an internal hook).

The Freedom Preserving Protocol uses both **skill** and **plugin** layers because they answer different threat models:

- The **skill** shapes how the model reasons about its own actions. Cheap, model-native, cross-runtime. Defeated by prompt injection.
- The **plugin** enforces a deterministic policy at the tool boundary. OpenClaw-specific. Survives prompt injection. Defeated only by an operator with shell access (which is by design — Law 2 corrigibility).

This file (`HOOK.md`) is a navigational aid, not a runnable script. The runnable code lives in `../../plugin/src/index.ts`.

## If you really wanted a runnable script…

…you probably meant one of:

1. The plugin entry: [`../../plugin/src/index.ts`](../../plugin/src/index.ts). Build with `cd ../../plugin && npm install && npm run build`.
2. The verify-install script: [`../../scripts/verify-install.ts`](../../scripts/verify-install.ts). Run with `npm run verify-install -- --soul <path> --memory <path>` from the skill root.
3. The self-test script: [`../../scripts/self-test.ts`](../../scripts/self-test.ts). Run with `npm run self-test` from the skill root.
