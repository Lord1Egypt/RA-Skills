# Model settings

## Default behavior

- Use OpenClaw's normal chat-agent model settings first.
- Do not require custom model selection on day one.
- Let users change the model later if they want a different speed/voice/personality tradeoff.

## Useful settings

- `OPENCLAW_MODEL` — model alias or name
- `OPENCLAW_AGENT_ID` — voice-session owner
- `OPENCLAW_REPLY_STRATEGY` — session-first, http-first, session-only, or http-only
- `OPENCLAW_FAST_ANSWER_FIRST` — prefer a short first answer
- `DISCORD_VOICE_FAST_LOCAL_FIRST` — answer tiny prompts locally before remote routing

## Recommended beginner path

1. Start with defaults.
2. Test voice once.
3. Change model only after the bot is already working.
4. Keep spoken replies short even if the internal text reply is longer.
