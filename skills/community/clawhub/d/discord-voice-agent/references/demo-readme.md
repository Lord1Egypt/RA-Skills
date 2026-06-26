# Discord Voice Agent for OpenClaw

Turn Discord into a living voice interface for OpenClaw — fast to install, easy to understand, and built to feel like a normal chat agent in voice.

This skill gives you a voice bot that can join a channel, listen, transcribe, reason with OpenClaw, and speak back with short, natural responses. It feels like a normal chat agent — just in voice.

## Why people will care

Most voice bots are either:

- too hard to set up
- too slow to feel alive
- too fragile to use in real conversations

Discord Voice Agent is built to feel different:

- quick to install
- easy to understand
- opinionated defaults
- reliable fallbacks
- short, voice-friendly replies
- great for demos, servers, and live helpers
- feels like something you can keep using, not just demo once
- designed to let beginners succeed without model confusion

## What it can do

- join and leave Discord voice channels
- capture speech per speaking turn
- transcribe speech with Whisper.cpp paths
- route the reply through OpenClaw
- use session-backed replies when healthy
- fall back to HTTP or local replies when needed
- keep spoken output short
- show status and history for debugging

## Install checklist

### If Discord is already installed

You usually only need:

- the voice channel id

Then start the bot and test a short voice turn.

Quick checklist:

1. Confirm Discord integration is already present.
2. Set the voice channel id.
3. Keep the default OpenClaw model.
4. Run the smoke check.
5. Try one short voice turn.

### If Discord is not installed yet

You need:

- the Discord plugin/integration
- Discord token
- voice channel id
- optional guild id

Then start the bot and verify it can join voice.

Quick checklist:

1. Install the Discord plugin/integration.
2. Add the token.
3. Set the voice channel id.
4. Leave the model on the default OpenClaw chat behavior.
5. Run the smoke check.

No model picking needed on day one — it can use the normal OpenClaw chat model defaults first.

## First-run wizard

1. Confirm whether Discord is already installed.
2. Enter only the missing setup.
3. Keep the default OpenClaw model first.
4. Run the smoke check.
5. Try one live voice turn.

## How it uses AI

The skill does not hard-code a model.
It sends the transcript and context to OpenClaw, then OpenClaw selects the configured reply path/model.
By default, it behaves like OpenClaw’s normal chat agent; you can change the model later if you want.

Suggested model settings:

- start with the default OpenClaw chat model
- keep `OPENCLAW_REPLY_STRATEGY=session-first` when possible
- switch to a custom model only after the bot is already working

Recommended order:

1. session-backed OpenClaw reply
2. HTTP OpenClaw reply
3. local/simple fallback for tiny prompts

## What makes it feel premium

- replies stay short enough for live speech
- simple prompts answer fast
- long replies get compacted before TTS
- acks stay brief and non-annoying
- disconnects and bad captures can recover cleanly
- `/status` makes the bot feel trustworthy
- the default behavior feels like a normal chat agent, not a special-case voice demo

## Great demo use cases

- server helper that answers questions out loud
- meeting companion for a Discord voice room
- live research buddy for OpenClaw users
- lightweight local voice assistant for modest hardware
- voice Q&A bot with real fallback behavior

## Troubleshooting

- No voice? Check token, permissions, and voice channel id.
- No reply? Check OpenClaw routing and the status server.
- Too slow? Lower reply length and keep fast-local-first enabled.
- Bad audio? Check ffmpeg, Whisper model path, and capture output.

## Best next upgrades

- better reconnect/rejoin handling
- faster response previews
- richer status/health metrics
- cleaner voice interruption handling
- improved onboarding for new installs
- a real first-run wizard in the UI
- a dedicated model settings panel
- richer smoke-test diagnostics
- publish a polished release page and demo video
