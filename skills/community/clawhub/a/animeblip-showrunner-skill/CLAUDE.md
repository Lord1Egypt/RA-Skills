# CLAUDE.md

Guidance for Claude Code (and any agent) when **working on** the animeblip-showrunner-skill repo.

## What this is

This repo is the **Animeblip Showrunner skill package** — a set of Python scripts + a
`SKILL.md` behavior guide, installed into `~/.claude/skills/` and invoked by an agent
(Claude Code / OpenClaw / etc.). It is **not** a backend service: the scripts wrap HTTP
calls to Animeblip's REST API (the same endpoints the Animeblip MCP server wraps).

The backend is Animeblip's own service (host `https://studio.animeblip.com`). When you change
a field, route, or enum here, the matching capability must already be live on the backend —
otherwise the script call returns 400/404.

## Architecture

```
SKILL.md            ← behavior contract: when the agent triggers, how it chains scripts, the flow, triage, rules
README.md           ← user-facing: install, setup, layout
skill-card.md       ← one-screen command quick-reference
scripts/_common.py  ← the ONLY shared layer: urllib HTTP + Bearer auth + one api_* wrapper per endpoint
scripts/*.py        ← one script = one action; thin argparse + _common call + print_json shell
docs/               ← deep-dive concept docs (triage-rules, cost-model-and-caps)
```

**Python standard library ONLY.** `_common.py` uses `urllib.request` on purpose — a skill
installed on a user's machine must not require `pip install`. Never introduce
requests/httpx/pydantic or any third-party package.

Each script is the same thin shell:
1. `sys.path.insert(0, os.path.dirname(__file__))`, then import from `_common`
2. `argparse` for args
3. call the `_common` api_* wrapper
4. `print_json(result)` — the caller (agent) parses stdout

When you add an API call, **first add an `api_*` wrapper in `_common.py`** (mirror
`api_send` / `api_create_story`), then write the thin script. Don't let a script build its
own URL/headers.

## SKILL.md is the source of behavior

`SKILL.md` is the agent's runbook — it defines the command table, the instruction-driven
flow, triage rules, and the rules. **When you change a script's name/args or add a script,
update SKILL.md's command table AND skill-card.md AND README.md's layout in the same edit**,
or the agent's behavior drifts from the actual scripts.

## Design decisions (don't undo without being asked)

- **Instruction-driven, no managed loop.** The agent drives by polling `query_session.py`
  and sending `send_message.py` — end-to-end vs step-by-step is decided by WHAT message is
  sent, not a flag. There is deliberately no `run_loop.py` / `showrunner.py` dispatcher /
  `approve.py` (all removed). Don't reintroduce a forced loop.
- **Naming mirrors the model:** Story = episode, Series = project. `create_project.py` =
  new series + episode 1; `create_episode.py` = next episode in an existing series.
- **Spend is bounded by guidance, not hard caps** (~2 retries/shot, ~6 fix-sends/episode →
  surface to human). It's judgment, not enforced state.

## Common commands

No lint, no tests, no build. Day-to-day:

```bash
export ANIMEBLIP_API_KEY="ab_…"                       # your Animeblip API key — create one at studio.animeblip.com → API Keys
export ANIMEBLIP_BASE_URL="https://studio.animeblip.com"   # optional — defaults to prod

python3 scripts/create_project.py --title "Test" --dry-run   # --dry-run never spends
python3 scripts/query_session.py --story <storyId>
python3 -m py_compile scripts/*.py                            # the only "test" — must stay clean
```

`--dry-run` works on every command and never spends credits — use it to verify wiring.

## Conventions

- **Do NOT `git commit`** unless the user explicitly asks.
- Keep scripts thin — logic that isn't one HTTP call belongs in `_common.py` or `SKILL.md`,
  not in a script.
- When refactoring, delete old logic outright (no back-compat) unless the user asks to keep it.
- After any script rename/removal, grep the whole skill for stale references and update
  SKILL.md / README.md / skill-card.md / docs together.
