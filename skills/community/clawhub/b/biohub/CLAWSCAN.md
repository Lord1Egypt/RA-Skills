# Clawscan note — biohub v0.5.0

Read-only adapter between an LLM agent and the user's local SQLite
health DBs. **No network I/O, no credential handling, no dynamic
execution, no writes to user data.** Every action the skill instructs
the agent to run is a `SELECT` against
`$OPENCLAW_BIOHUB_HOME/data/health.db`.

## Threat model

| Capability | Status | Note |
|---|---|---|
| Network access | None | All data is local SQLite. |
| Credentials | None | OAuth tokens for adapters (WHOOP/Oura/Fitbit/Garmin) + the Libre/Apple-Health file-watch paths are written by the separate `biohub` CLI — out of this skill's surface. |
| Dynamic exec | None | No `eval`, `exec`, `pickle.loads`, `Function(...)`. |
| File writes | None by the skill itself. It suggests an optional workspace-local `memory/` directory; never writes biometric data into shipped files. |
| Shell shown | `sqlite3 "$HEALTH_DB" "SELECT ..."` only. Read-only on the user's own DB. No user input concatenated into commands. |
| Domain | Health / biometrics — see below. |

## What a scanner may flag, and why it's expected

1. **OAuth / API names: WHOOP, Oura, Fitbit, Garmin, Apple Health.**
   The skill *describes* these adapters and tells the agent to suggest
   `biohub connect <slug>` to the user. The skill never calls any of
   them. All network I/O lives in the `biohub` Python CLI, not here.
2. **Shell blocks in code samples.** SKILL.md contains
   `sqlite3 "$HEALTH_DB" "..."` recipes. These are documentation shown
   to the agent — not parameterized injection points. All queries are
   literal `SELECT`s; nothing user-controlled gets concatenated.
3. **Env-var references** (`$OPENCLAW_BIOHUB_HOME`, `$HEALTH_DB_PATH`).
   Path locators only. The skill never reads env vars holding secrets.
4. **"credentials" / "secrets" strings.** Appear in defensive guidance
   ("never write biometric data into public files"). The skill is the
   consumer of that guidance, not a secret-handler.
5. **Medical / health language.** Personal-biometrics domain (HRV,
   body fat %, blood markers, glucose, biological age). **Not medical
   software**; disclaimer is in SKILL.md and pinned at
   https://github.com/maxnau89/openclaw-biohub/blob/main/DISCLAIMER.md.
6. **A localhost HTTP listener** (`adapters.apple_health.receiver`, for
   the Health Auto Export iOS app) exists in the backing software. It is
   part of the `biohub` package, **not this skill** — the skill never
   starts it, binds no port, and opens no socket. It binds 127.0.0.1 with
   bearer-token auth by default. Same boundary as the OAuth adapters:
   documented here, invoked only by the CLI.

## Health-data handling

Biometrics live in **local SQLite files** under
`$OPENCLAW_BIOHUB_HOME/data/`. They never leave the user's machine
via this skill — the agent reads them in-process and discusses them
with the user. SKILL.md explicitly instructs the agent to never write
user-identifying biometric data into files that get committed to a
public repo or shipped with a ClawHub install.

If the host's LLM provider sends prompt context to a remote model
(Claude API, OpenAI API, etc.), the data crosses the network there —
that's the host's chosen-provider responsibility, not the skill's.
The skill itself is a strictly local consumer.

## Provenance

| | |
|---|---|
| Repo | https://github.com/maxnau89/openclaw-biohub |
| License | MIT (skill + backing software) |
| Tests | 167 Python + 33 dashboard, all green |
| Release | https://github.com/maxnau89/openclaw-biohub/releases/tag/v0.5.0 |
| CI | https://github.com/maxnau89/openclaw-biohub/actions |
| Maintainer | github.com/maxnau89 |
