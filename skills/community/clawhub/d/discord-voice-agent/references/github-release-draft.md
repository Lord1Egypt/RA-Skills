# GitHub Release Note — Discord Voice Agent v1.0.1

## Summary

Discord Voice Agent turns OpenClaw into a live Discord voice assistant: join a voice channel, capture speech, transcribe it, route the reply through OpenClaw, and speak back with short, natural responses. It is designed to feel like a normal chat agent in voice, not a fragile demo.

## Highlights

- beginner-friendly first-run flow
- works with existing Discord installs
- only asks for missing setup
- default OpenClaw chat-model behavior first
- model settings can be changed later
- one-command smoke test
- short voice-friendly replies
- fallback behavior for STT/TTS/Discord/OpenClaw failures
- status/history/debug guidance
- beginner-friendly setup with minimal required input

## Quick install

### Existing Discord install

1. Set `DISCORD_VOICE_CHANNEL_ID`.
2. Keep the default OpenClaw model.
3. Run `npm run smoke`.
4. Try `/status`, `/say`, then one short voice turn.

### Fresh Discord install

1. Install the Discord plugin/integration.
2. Set `DISCORD_TOKEN`.
3. Set `DISCORD_VOICE_CHANNEL_ID`.
4. Optionally set `DISCORD_GUILD_ID`.
5. Keep the default OpenClaw model.
6. Run `npm run smoke`.

## Why it matters

This release is designed to feel like a normal chat agent in voice, not a fragile demo. Beginners can get started without choosing a model on day one, and advanced users can tune the routing later. The default path is simple: use OpenClaw’s normal chat model settings first, then customize if you want.

## Files worth linking

- demo README: `references/demo-readme.md`
- quickstart: `references/quickstart.md`
- wizard: `references/wizard.md`
- model settings: `references/model-settings.md`
- release checklist: `references/release-checklist.md`
