---
name: dlazy-start
version: 2.0.0
description: Quickstart for AI orchestrators (Claude Code / Cursor / Codex / Copilot) driving @dlazy/cli. Covers install, auth, capability discovery, invoking cloud + local tools, polling async tasks, and recovering from common failures.
triggers:
  - dLazy CLI Quickstart for AI Agents
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli","installAlternative":"npx @dlazy/cli","homepage":"https://dlazy.com","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"AGPL-3.0-or-later","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"You are operating @dlazy/cli for the user. Discovery first: run `dlazy tools list` to see available tools and `dlazy tools describe <name>` to inspect a tool's input/output schema and cost shape. Invoke with `dlazy <tool-name> --input @file.json` (or `--output json` for machine-readable envelopes). Poll long-running cloud tasks with `dlazy status <generateId>`. Install optional local runtimes with `dlazy doctor remotion --install` or `dlazy doctor yt-dlp --install`. Never claim a tool exists without verifying via `dlazy tools list`."}}
---

# dlazy-start — Quickstart for AI Agents

[English](./SKILL.md) · [中文](./SKILL-cn.md)

A minimal contract for AI orchestrators using `@dlazy/cli`. The CLI is a
tool-dispatch surface: every registered cloud + local tool becomes a top-level
subcommand. There is no built-in project workspace or pipeline state machine —
those are agent-side concepts.

License: AGPL-3.0-or-later.

## What this skill teaches

You drive `@dlazy/cli` from auth through tool invocation:

- **Cloud tools** (40+) — image / video / audio / text providers (Seedream,
  Recraft, MJ, Veo, Seedance, Kling, ElevenLabs, …)
- **Local tools** (40+) — `state_lock_profile`, `video_compose`,
  `post_render_gate`, `scene_detect`, `frame_sampler`, `audio_mixer`,
  `audio_probe`, `transcribe`, `subtitle`, `color_grade`, `extract_segment`,
  `ffmpeg_run`, … (full list via `dlazy tools list`)
- **CLI commands**: `auth`, `doctor`, `tools list`, `tools describe`,
  `status`, plus one top-level subcommand per registered tool.

---

## Phase 0 — Install & auth

```bash
# Install once
npm install -g @dlazy/cli

# Authenticate (device-code flow; works in remote shells)
dlazy auth login
```

Alternate auth: `dlazy auth set YOUR_API_KEY`, or set the `DLAZY_API_KEY`
env var. Config lives at `~/.dlazy/config.json` (Windows:
`%USERPROFILE%\.dlazy\`).

Global flags every command accepts: `--api-key`, `--base-url`, `--verbose`,
`--output <json|url|text>`, `--refresh-manifest`, `-l/--lang <locale>`.

---

## Phase 1 — Discover capabilities

```bash
dlazy --help                         # top-level command surface
dlazy tools list                     # registered tools with type + cost shape
dlazy tools describe <name>          # input/output JSON schema, hasCosts, examples
```

Optional local runtimes need a one-time install:

```bash
dlazy doctor remotion                # report Remotion composer state
dlazy doctor remotion --install      # ~50s, installs the bundled composer

dlazy doctor yt-dlp --install        # for video_downloader on YouTube et al.
dlazy doctor yt-dlp --install --proxy http://127.0.0.1:1087
```

Some sandboxes restrict the tool surface via `DLAZY_DISABLED_TOOLS=<csv>`;
disabled tools are hidden from `dlazy --help` and refuse invocation with a
clear `tool_disabled` error.

---

## Phase 2 — Invoke a tool

Every tool is a top-level subcommand:

```bash
# Inline flags (mirrors the input schema)
dlazy gpt-image-2 --prompt "cyberpunk cat at dusk"

# JSON input file (preferred for complex shapes)
dlazy video_compose --input @work/compose.json --output json

# Dry-run for validation only (no remote call, no credit consumption)
dlazy seedance-2-0 --input @plan.json --dry-run
```

Per-tool help is generated from the schema:

```bash
dlazy <tool-name> --help
```

Output modes:

- `--output text` (default) — human-readable envelope
- `--output json` — single JSON line per call; parse with `jq`
- `--output url` — bare URL when the tool produces a single asset

---

## Phase 3 — Poll async cloud tasks

Long-running generations return a `generateId` instead of the final asset:

```bash
dlazy status <generateId>
dlazy status <generateId> --output json
```

Repeat until status is `succeeded` (then the asset URL is in the payload) or
`failed` (with `error.code` + `error.message`).

---

## Phase 4 — Common failure recovery

**`dlazy doctor remotion --install` fails on `npm install`:**
- Check Node ≥ 18 (`node --version`).
- Behind a corp proxy: set `npm_config_proxy` / `npm_config_https_proxy`.

**`video_downloader` returns "Sign in to confirm you're not a bot":**
- YouTube anti-bot challenge. Pass `"cookies_from_browser": "chrome"`
  (or firefox / safari / edge) in the input JSON.

**`video_compose` returns "render_runtime=hyperframes not yet implemented":**
- HyperFrames runtime not shipped. Switch `edit_decisions.render_runtime` to
  `remotion` or `ffmpeg`, then re-validate via `pre_render_validator`.

**ElevenLabs STT returns an empty `words` array:**
- Pass `timestamps_granularity: "word"` explicitly.

**Need to know a tool's cost before invoking:**
- `dlazy tools describe <name>` exposes `hasCosts` and the cost shape. Log
  the estimate to a local file or your audit log before calling the tool.

**Unknown command suggestion:**
- `dlazy <typo>` returns `error: unknown command '<typo>'` plus a "Did you
  mean …?" suggestion line based on edit distance. Trust the suggestion only
  after confirming via `dlazy tools list`.

---

## Anti-patterns

- Calling a tool whose existence you haven't verified via `dlazy tools list`.
- Memorizing provider names from prior sessions instead of re-checking the
  registry (tools come and go).
- Silently swapping render runtime mid-pipeline (govern via `state_lock_profile`
  + `post_render_gate` parity checks instead).
- Calling paid generation without announcing provider / model / cost first.

---

## Reference card

```
INSTALL       npm install -g @dlazy/cli && dlazy auth login
DISCOVER      dlazy tools list  |  dlazy tools describe <name>
LOCAL RT      dlazy doctor remotion --install   (or yt-dlp)
INVOKE        dlazy <tool-name> --input @file.json --output json
DRY RUN       dlazy <tool-name> --input @file.json --dry-run
POLL          dlazy status <generateId>
HELP          dlazy --help  |  dlazy <tool-name> --help
RECOVER       dlazy doctor <target>  |  dlazy tools describe <name>
```
