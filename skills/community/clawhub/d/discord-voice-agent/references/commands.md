# Discord Voice Agent commands and knobs

## Core commands

- `npm run smoke` — cheap pipeline check
- `npm test` — full test suite
- `npm start` — run the bot
- `node src/index.js start` — direct start
- `node src/index.js smoke` — direct smoke path

## Main behaviors

- Discord slash commands: `/join`, `/leave`, `/say`, `/status`, `/help`
- Voice receive/capture with per-turn saved audio
- Whisper.cpp STT path with safe fallback handling
- OpenClaw reply routing with configurable session-first/http-first behavior
- Short spoken replies and acknowledgement cooldowns
- Local status/history server

## Important env vars

- `DISCORD_TOKEN`
- `DISCORD_VOICE_CHANNEL_ID`
- `DISCORD_VOICE_AUTO_JOIN`
- `DISCORD_VOICE_AUTO_RESPOND`
- `DISCORD_VOICE_RESPOND_TO_ALL`
- `DISCORD_VOICE_WAKE_PHRASE`
- `DISCORD_VOICE_ACK_ENABLED`
- `DISCORD_VOICE_ACK_TEXT`
- `DISCORD_VOICE_ACK_COOLDOWN_MS`
- `DISCORD_VOICE_REPLY_MAX_CHARS`
- `DISCORD_VOICE_REPLY_MAX_SENTENCES`
- `DISCORD_VOICE_FAST_LOCAL_FIRST`
- `OPENCLAW_BASE_URL`
- `OPENCLAW_GATEWAY_TOKEN`
- `OPENCLAW_MODEL`
- `OPENCLAW_AGENT_ID`
- `OPENCLAW_REQUEST_TIMEOUT_MS`
- `OPENCLAW_REPLY_STRATEGY`
- `FFMPEG_PATH`
- `WHISPER_BIN`
- `WHISPER_MODEL`
- `WHISPER_LANGUAGE`
- `DISCORD_TTS_VOICE`

## Output locations

- `.kittu-voice-history/` — local JSONL conversation history
- `.kittu-voice-captures/` — captured voice turns
- status server — defaults to port `8787`
