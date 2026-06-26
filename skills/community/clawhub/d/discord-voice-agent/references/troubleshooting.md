# Discord Voice Agent troubleshooting

## Fast checks

1. Confirm Discord token and voice channel env vars are set.
2. Run `npm test`.
3. Run `npm run smoke`.
4. Check the status server and recent history.

## Common problems

### Bot joins but stays silent
- Check auto-respond settings.
- Check STT binary/model paths.
- Verify voice capture is producing files.
- Confirm OpenClaw reply routing is reachable.

### Replies are too long or slow
- Lower `DISCORD_VOICE_REPLY_MAX_CHARS`.
- Lower `DISCORD_VOICE_REPLY_MAX_SENTENCES`.
- Keep `DISCORD_VOICE_FAST_LOCAL_FIRST=true` for simple prompts.
- Prefer session-backed replies only if OpenClaw is healthy.

### Capture or STT fails
- Check ffmpeg availability.
- Check Whisper model path.
- Inspect saved captures for bad audio turns.
- Confirm the turn is not filtered as too short.

### Discord voice disconnects
- Verify reconnect/rejoin logic.
- Clear orphaned runtime artifacts.
- Restart only the bot process, not the whole machine.

## Debug order

- First: status server / logs
- Second: test suite
- Third: captured audio + transcript history
- Fourth: OpenClaw routing configuration
- Fifth: Discord permission / voice channel setup
