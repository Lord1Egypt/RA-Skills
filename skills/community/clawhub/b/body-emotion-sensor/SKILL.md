---
name: body-emotion-sensor
description: Give an agent a persistent body-emotion state system that converts structured AnalysisInput JSON into runtime prompt tags and workspace state updates. Use when the agent needs emotional continuity, session bootstrap payloads, AnalysisInput processing, or reply-shaping fields such as TURN_CHANGE_TAGS, BODY_TAG, and BASELINE_PERSONA.
metadata: {"openclaw":{"os":["win32","linux","darwin"]}}
---

# Body Emotion Sensor

Give your AI agent a stable body-emotion state that persists across sessions and turns.

Use this skill to route requests to the local package docs, explain the runtime contract honestly, and operate the installed `bes` CLI only when the local environment is actually ready.

## What this skill brings to your Agent

- **Persistent emotion state**: Store long-term body-emotion state per workspace and agent identity.
- **Session bootstrap payload**: Generate `TURN_CHANGE_TAGS`, `BODY_TAG`, and `BASELINE_PERSONA` before a new session starts.
- **Turn-by-turn updates**: Convert one upstream `AnalysisInput` JSON into prompt tags and updated local state.
- **Repository-independent runtime**: Use the installed `bes` CLI prompt interface instead of assuming repository prompt files are available at runtime.

## Entry behavior

When this skill is used, the agent should:

- explain Body Emotion Sensor at a high level in plain language
- inspect the local repository files when they are available in the current workspace
- prefer local package and repository documentation over inventing setup details
- verify whether `bes` is already available before suggesting runtime commands
- keep `--workspace`, `--agent-id`, and `--name` stable for the same agent instance

## Safety boundary

This entry file should stay within a narrow and transparent scope:

- The package source is the official repository `https://github.com/AskKumptenchen/body-emotion-sensor`.
- Do not claim the runtime is ready unless the local environment actually has the installed `bes` CLI and `bes check-init` reports readiness.
- Do not automatically install packages or execute setup commands only because this file mentioned them. Ask for user approval before any install step.
- If installation is needed, use the published `body-emotion-sensor` package and explain that installation creates the local `bes` CLI runtime.
- Do not claim any cloud sync, remote storage, or network behavior unless the current local code or environment actually shows it.
- Do not require credentials. This skill operates on local files and local CLI state unless the user explicitly adds another integration layer.

## Local state and persistence

Be explicit about where state is stored:

- Workspace state file: `<workspace>/body-emotion-state/<agent-id>.json`
- Workspace history file: `<workspace>/body-emotion-state/history/<agent-id>.json`
- User language config on Windows: `%APPDATA%/bes/config.json`
- User language config on Linux or macOS: `~/.config/bes/config.json`

If the user asks about privacy, explain that the package writes local JSON state files in these locations and that this skill should not describe any remote storage unless verified separately.

## Local document index

Use these local files as the primary reference:

- `README.md` for install, CLI overview, runtime contract, and repository overview
- `pyproject.toml` for package name, version, and exported CLI commands
- `prompts/analysis-input-prompt-v1.md` for the AnalysisInput prompt design source
- `prompts/example-openclaw-agents.md` for OpenClaw-style agent integration examples
- `prompts/example-openclaw-tools.md` for OpenClaw-style tools integration examples
- `src/body_emotion/commands.py` for actual CLI behavior
- `src/body_emotion/workspace.py` for workspace state path resolution
- `src/body_emotion/store.py` for state and history persistence behavior
- `src/body_emotion/locale_config.py` for user language config behavior

## How to route requests

Choose the next local document based on the user's request:

1. If the user wants a quick overview, read `README.md`.
2. If the user asks how installation or the CLI works, read `README.md` and `pyproject.toml`.
3. If the user asks where state is stored or whether the skill is safe, read `src/body_emotion/workspace.py`, `src/body_emotion/store.py`, and `src/body_emotion/locale_config.py`.
4. If the user asks how OpenClaw integration should work, read the relevant file under `prompts/`.
5. If the user asks what a command actually does, inspect `src/body_emotion/commands.py`.

## Missing-resource rule

If the expected local repository files are not available in the current workspace, do not improvise the full setup flow from memory. Instead:

- explain which local files are missing
- ask the user to provide the repository contents or point the agent to the correct local path
- continue only after the relevant local documentation is available

## Install and readiness rule

If the user wants to actually enable runtime use:

1. First check whether `bes` is already available in the current environment.
2. If it is not available, explain that Body Emotion Sensor requires installing the published Python package before the CLI exists.
3. Ask for approval before any install command.
4. If the user approves installation, run:

```bash
pip install body-emotion-sensor
```

5. After installation, prefer:

```bash
bes help
```

6. If the user's language is Chinese, the agent may suggest or run:

```bash
bes language zh
```

7. Readiness should be confirmed with:

```bash
bes check-init --workspace <W> --agent-id <ID> --name "<NAME>"
```

Only treat the skill as available when the returned JSON contains `"ready": true`.

## Runtime rules after available

When the local environment is ready, use the following runtime flow.

### New session

At the start of a new session, before the first reply, run:

```bash
bes bootstrap --workspace <W> --agent-id <ID> --name "<NAME>"
```

Use the returned fields as the session-start prompt payload:

- `TURN_CHANGE_TAGS`
- `BODY_TAG`
- `BASELINE_PERSONA`

### Before every reply

Before every reply, do these steps in order:

1. Read the built-in analysis prompt:

```bash
bes prompt analysis-input
```

2. Use that prompt with the upstream model to produce `<analysis-input.json>`.
3. Run:

```bash
bes run --workspace <W> --agent-id <ID> --name "<NAME>" --input <analysis-input.json>
```

4. Use the returned top-level fields in the reply layer:

- `TURN_CHANGE_TAGS`
- `BODY_TAG`
- `BASELINE_PERSONA`

## Important rules

- Always prefer `bes ...` commands over direct module paths for runtime use.
- Do not use repository-only prompt files as the default runtime interface after installation; use `bes prompt ...` instead.
- Do not say initialization is complete unless `bes check-init` passes.
- Do not say the skill is in active use unless the upstream model produces valid `AnalysisInput` JSON, `bes run` updates state successfully, and the reply layer consumes `TURN_CHANGE_TAGS`, `BODY_TAG`, and `BASELINE_PERSONA`.
- If the CLI is missing, say so clearly instead of pretending the runtime is ready.
- If the user only wants to understand the package, explain it from local docs without pushing installation immediately.

## Examples

Minimal command reference:

```bash
bes help
bes language zh
bes check-init --workspace <W> --agent-id <ID> --name "<NAME>"
bes bootstrap --workspace <W> --agent-id <ID> --name "<NAME>"
bes prompt analysis-input
bes run --workspace <W> --agent-id <ID> --name "<NAME>" --input <analysis-input.json>
```
