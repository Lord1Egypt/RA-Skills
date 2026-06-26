# daily-strava-roast

[![CI](https://github.com/ranasalalali/daily-strava-roast/actions/workflows/ci.yml/badge.svg)](https://github.com/ranasalalali/daily-strava-roast/actions/workflows/ci.yml)

A portable AgentSkill and Python CLI for turning recent Strava activity into a funny daily roast.

## Overview

`daily-strava-roast` reads recent Strava activity and turns it into a short recap with adjustable sarcasm.

It is built for:
- playful workout summaries
- scheduled daily activity roasts
- post-workout recaps with personality
- configurable tone and spice level
- slightly unnecessary but highly respectable levels of sass

## Quick start

```bash
uv run --project . daily-strava-roast roast
uv run --project . daily-strava-roast roast --tone playful --spice 3
uv run --project . daily-strava-roast summary --json --pretty
```

## Strava auth behaviour

This CLI is designed to be hands-off after initial setup.

Canonical config locations:
- app credentials: `~/.openclaw/secure/strava_app.json`
- tokens: `~/.openclaw/workspace/agents/tars-fit/strava_tokens.json`

Expected behaviour:
- if the token file exists and includes a valid `refresh_token`, expired access tokens are refreshed automatically
- if the activity fetch still returns `401`, the CLI forces one refresh and retries once
- if there is no token file, invalid token JSON, or required token fields are missing, the CLI returns `status: initial_setup_required`
- if the token file exists but app credentials are missing/incomplete, the CLI returns `status: config_incomplete`
- if refresh still fails after setup exists, the CLI returns `status: reauth_required`

Operational guidance:
- prefer the secure JSON config over shell startup files or ad hoc sourced env vars
- treat `~/.openclaw/secure/strava_app.json` as the one canonical place for Strava app credentials
- both the packaged CLI and the legacy script should read from that secure config by default
- do not commit secrets or token files

That gives an agent a reliable machine-readable split between:
- **first-time setup needed**
- **app config incomplete**
- **manual reauthorisation needed**
- **temporary Strava/network failure**

## Why it exists

There are already serious Strava integration and coaching skills.

This project exists for a far nobler purpose: making your training log entertaining enough to deserve being read.

## One canonical repo, two interfaces

This repo serves both as:
- a **portable AgentSkill** via `SKILL.md`
- a **small Python CLI** via the packaged `daily-strava-roast` command

That keeps the implementation, local use, and eventual publication aligned in one place.

## Features

- fetch recent Strava activity from a token file
- automatically refresh expired Strava access tokens using the stored refresh token
- retry once after a Strava 401 before giving up
- return a clear `initial_setup_required` status when first-time Strava setup is missing or incomplete
- return a clear `reauth_required` status when manual reauthorisation is needed
- target the local calendar day for daily roasts so no-activity days behave correctly
- summarize the day instead of dumping raw activity lines
- generate compact narrative roasts
- adjustable tone: `dry`, `playful`, `savage`, `coach`
- adjustable spice: `0..3` (default leans spicy)
- smarter no-activity roasts based on inactivity gap
- lightweight roast memory to reduce repetition over time
- richer recent-day roast state so future roasts can reference streaks, recent load, and prior-day context when it helps
- structured V2 context and prompt generation for runtime model use
- JSON summary output for scripting

## Repo structure

- `SKILL.md` — agent instructions
- `src/daily_strava_roast/cli.py` — packaged CLI entrypoint
- `references/design.md` — design notes and roast heuristics
- `tests/smoke_test.py` — fixture-based smoke test

## CLI usage

```bash
uv run --project . daily-strava-roast roast
uv run --project . daily-strava-roast roast --tone playful --spice 3
uv run --project . daily-strava-roast roast --tone coach --spice 0
uv run --project . daily-strava-roast summary --json --pretty
uv run --project . daily-strava-roast context --pretty
uv run --project . daily-strava-roast prompt
uv run --project . daily-strava-roast preview
uv run --project . daily-strava-roast roast
```

V2 staging note:
- `context` emits the structured roast context JSON
- `prompt` emits the constrained prompt text built from that context
- `preview` emits a local preview paragraph from the V2 context/prompt path for prompt-shape evaluation
- `roast` remains deterministic in the packaged CLI
- connected/default-model generation belongs to the OpenClaw runtime skill layer, not the standalone package CLI
- the intended runtime flow is: `context` -> `prompt` -> connected model paragraph -> fallback to deterministic `roast` when needed

## Example output

Deterministic roast example:

```text
Morning Ride: 56.95 km of ride in 150 min. A creative new way to be tired for no financial reward.
```

Runtime V2 target example:

```text
Morning Ride sounds like you were trying to file 56.95 km and 733 m of climbing under casual admin, which is an impressively committed way to pretend this hobby isn't just organised self-inflicted inconvenience.
```

## Testing

```bash
python tests/smoke_test.py
python tests/test_context_builder.py
python tests/test_prompt_builder.py
python tests/test_target_day.py
python tests/test_roast_memory.py
```

CI checks:
- CLI help
- smoke test execution
- package build

## Publish hygiene

Do not publish local runtime leftovers such as:
- `.venv/`
- `dist/`
- `state/`
- token files or any local secrets

A small `.clawhubignore` is included to document the intended exclusions for ClawHub publishing.

## Design goals

- portable
- local-first
- funny without becoming unreadable
- small and pragmatic
- suitable for both real use and eventual publication
