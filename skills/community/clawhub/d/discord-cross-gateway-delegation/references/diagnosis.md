# Diagnosis

## Known-good findings from this setup pattern

The following symptoms mean different things:

### Symptom: controller bot cannot send to the channel

Likely causes:

- bot not invited to server
- bot not added to private channel
- permission modal change not saved

### Symptom: worker can see the private channel but never auto-replies

Likely causes:

- worker bot treats guild channels differently from DMs
- worker gateway inbound policy blocks server-channel input
- worker allowlist/guild filtering excludes this server/channel
- worker is configured as DM-first only
- worker preflight drops bot-authored task envelopes before they reach the processing stage

### Symptom: worker responds in DM but not in the private channel

This is the most important diagnostic split.
It means:

- the bot is alive
- Discord token/gateway are fine
- inbound works at least in DM
- the remaining issue is almost certainly **guild/server-channel inbound policy**
- in live debugging, also check whether bot-authored worker envelopes are being dropped in preflight before process-time worker handlers can run

## Most likely config areas to inspect on the worker gateway

Priority order:

1. `groupPolicy`
2. `allowFrom`
3. `guilds`
4. `inboundWorker`

Check both account-scoped and global Discord config paths when relevant:

- `channels.discord.accounts.default.groupPolicy`
- `channels.discord.accounts.default.allowFrom`
- `channels.discord.accounts.default.guilds`
- `channels.discord.accounts.default.inboundWorker`
- `channels.discord.groupPolicy`
- `channels.discord.allowFrom`
- `channels.discord.guilds`
- `channels.discord.inboundWorker`

## Recommended temporary fallback

If the worker bot replies in DM but not in guild channels:

- do not block the project on config work
- switch to **DM-based delegation** immediately
- keep the structured task protocol unchanged
- revisit guild-channel config later when the worker machine is reachable

## Final-stage relay failure split

### Symptom: worker replies correctly in the lane but the final answer never returns to the original DM

Likely causes:

- controller-side result bridge is not active in the live runtime
- worker final reply is not emitted in a relay-friendly format
- worker reply lacks reply-reference or metadata needed for correlation
- controller bridge ignores `started` correctly but fails to catch the final reply

Meaning:

- setup is only partially complete
- the remaining bug is usually on the **controller-side result bridge**, not on the worker-side intake
