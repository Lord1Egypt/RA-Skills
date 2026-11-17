# Make it automatic — paste this into your project's instruction file

One file, three platforms. Hermes, OpenClaw and DeepSeek Harness all load a **workspace instruction
file at session start**, so a few lines there are enough to make memory recovery run on its own —
no code, no hooks, no config.

| Platform | File it loads at session start |
|---|---|
| **Hermes** | `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first match wins) + `SOUL.md` |
| **OpenClaw** | `AGENTS.md` in the workspace (runtime-provided startup context) |
| **DeepSeek Harness** | `AGENTS.md`-compatible files (agent-instructions plugin, walks up to the project root) |
| **Claude Code / Cursor / Codex** | `CLAUDE.md` / `.cursorrules` / `AGENTS.md` conventions |

## The block to paste

```md
## Session start — memory recovery (changsheng)

At the start of every new session, before anything else, follow the `changsheng-agent-memory` skill
(`SKILL.md`) as written:

1. stat/discover the memory carriers (re-discover if a path moved)
2. read the always-loaded layer in full
3. hash-check the conditional layer and read only what changed
4. restate the imperative rules (do / don't) before acting
5. if a ledger exists (`.changsheng/ledger.json`), run `python scripts/memory_ledger.py --check` and report any expired or over-budget rows
6. reply with one short line so the user knows recovery ran — e.g. "Memory recovered — ready."

Then handle the user's request. Do not skip step 6: it is how the user can tell recovery happened.
```

## If your platform has no workspace instruction file

Just say **"recover memory"** (or "接着上次") at the start of a session — the skill runs the same
procedure on demand.
