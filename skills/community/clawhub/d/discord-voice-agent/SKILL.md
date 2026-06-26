---
name: discord-voice-agent
description: Use when building, configuring, running, debugging, or extending a Discord voice agent integrated with OpenClaw, including first-time setup, voice capture, transcription, TTS, slash commands, reply routing, health/status, and release work.
---

# Discord Voice Agent

A practical OpenClaw skill for building and operating a Discord voice bot that listens, reasons, and speaks back like a normal chat agent, with short, reliable replies.

## Start here

Use this skill when the user wants a Discord voice agent that feels easy to install and easy to operate.

### Ask for only what is missing

- **If Discord is already installed:** ask only for the voice channel id.
- **If Discord is not installed:** require the Discord plugin/integration first, then ask for:
  - Discord token
  - voice channel id
  - optional guild id
- Detect OpenClaw settings from the environment when possible.
- Prefer sane defaults over extra setup.
- Default to OpenClaw’s normal chat-model settings unless the user changes them later.

## First-run wizard

Follow the wizard flow in `references/wizard.md`:

1. Detect whether Discord is already installed.
2. Ask only for missing setup.
3. Confirm the model default or custom model choice.
4. Verify voice join, `/status`, and one short test reply.
5. Ask for the next missing piece only if the first test fails.

## Beginner-friendly goal

Make the first working turn obvious:

1. bot joins the voice channel
2. bot hears a short test phrase
3. bot replies briefly
4. status clearly shows what happened

If anything fails, explain the missing piece in plain language.

## What this skill should help with

- new install and first-run setup
- Discord voice join and leave
- slash commands and voice playback
- STT/TTS troubleshooting
- OpenClaw reply routing
- latency reduction and fallback tuning
- release planning and upgrade work

## Core behavior

- join voice reliably
- capture speech per turn
- transcribe with the configured STT path
- route replies through OpenClaw
- speak back with short responses
- fall back cleanly when STT, TTS, Discord, or OpenClaw fails

## How the AI model is used

The skill itself does **not** choose a standalone model.
It sends transcript context to OpenClaw, and OpenClaw picks the reply path/model from config.

Use these rules:

- prefer session-backed replies when healthy
- fall back to HTTP or local replies when configured
- use the project’s OpenClaw model/agent settings, not hard-coded model names
- keep spoken output short, even if the text reply is longer internally
- enable fast-answer-first behavior for short questions when available
- treat the model like a normal chat-agent default first; let users change it later if they want

See `references/model-routing.md` and `references/model-settings.md` for the routing picture.

## Working rules

1. Start by checking the current project state and config.
2. Keep commands and setup copy-paste friendly.
3. Keep spoken replies brief.
4. Surface failures clearly.
5. Validate with tests or smoke checks before claiming success.
6. Use the one-command smoke path before asking users to do a live voice trial.

## Reference files

- `references/quickstart.md` — install and first-run flow
- `references/wizard.md` — guided onboarding flow
- `references/model-routing.md` — how the AI model is used
- `references/model-settings.md` — default vs custom model setup
- `references/test-mode.md` — one-command smoke path
- `references/troubleshooting.md` — common failures and fixes
- `references/upgrades.md` — best next upgrades
- `references/release-checklist.md` — release polish before publish
- `references/github-release-draft.md` — public release post draft
- `references/demo-video-script.md` — short demo video script

## What a great version looks like

- a new user can install and speak to it fast
- existing Discord installs only need the voice channel id
- missing Discord setup is detected cleanly
- the AI routing is understandable and configurable
- voice replies feel fast, short, and natural
- failures are recoverable instead of silent
