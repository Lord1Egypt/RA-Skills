# `clawhub` — DanceTempo context skill (ClawHub / Cursor)

This folder is the **authoritative** copy of the **ClawHub + DanceTempo** agent skill. It is versioned inside the [DanceTempo](https://github.com/arunnadarasa/dancetempo) repository under `.cursor/skills/clawhub/`.

## Purpose

- Point agents at **`public/llm-full.txt`** (full repo bundle) and **`CLAWHUB.md`** (tribal debugging).
- Document Tempo + MPP + server patterns without duplicating the whole README.

## Publishing to ClawHub

1. Zip **this entire folder** (`clawhub/`) so uploads include:
   - `SKILL.md`
   - `README.md` (this file)
   - `references/*`
   - `assets/*`
   - `scripts/*`
   - `hooks/openclaw/*`
2. Optionally set **`_meta.sample.json`** → rename to **`_meta.json`** and fill fields **after** ClawHub provides IDs (or use the site UI only).

## Layout (compare: self-improving-agent)

| self-improving-agent | dancetempo-clawhub |
| --- | --- |
| `.learnings/*` templates | Use repo **`CLAWHUB.md`** instead |
| `hooks/openclaw/*` | **`hooks/openclaw/`** — `dancetempo-clawhub` bootstrap reminder (see **`HOOK.md`**) |
| `references/examples.md` | **`references/examples.md`** |
| `scripts/*.sh` | **`scripts/verify-dancetempo-context.sh`** |

## Maintenance

When **`scripts/build-llm-full.mjs`** gains or loses files, update **`assets/LLM-BUNDLE-SOURCES.md`** and run **`npm run build:llm`**.
