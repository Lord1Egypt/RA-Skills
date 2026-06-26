# Quickstart

## Existing Discord install

If Discord integration is already available in OpenClaw:

1. Set `DISCORD_VOICE_CHANNEL_ID`.
2. Set OpenClaw reply settings if needed.
3. Run the bot.
4. Join the voice channel and test `/status` and `/say`.

## Fresh Discord setup

If Discord integration is not available yet:

1. Install the Discord plugin/skill first.
2. Set `DISCORD_TOKEN`.
3. Set `DISCORD_VOICE_CHANNEL_ID`.
4. Optionally set `DISCORD_GUILD_ID`.
5. Set OpenClaw routing variables.
6. Run tests and smoke checks.

## Minimum recommended config

- `DISCORD_TOKEN`
- `DISCORD_VOICE_CHANNEL_ID`
- `OPENCLAW_BASE_URL`
- `OPENCLAW_AGENT_ID`
- `OPENCLAW_REPLY_STRATEGY`

## Model default

You do not need to pick a custom model on day one.
If OpenClaw is already configured, use its normal chat-agent model settings first and change them later only if you want different behavior.

## One-command test mode

Run:

```bash
npm run smoke
```

Then, if that passes, run a live check with `/status` or `/say`.

## First checks

- `npm test`
- `npm run smoke`
- confirm the status server starts
- confirm the bot can join and speak once
