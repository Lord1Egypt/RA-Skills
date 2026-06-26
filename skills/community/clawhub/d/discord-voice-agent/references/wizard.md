# First-run wizard flow

Use this flow to keep onboarding simple.

## 1. Detect Discord state

Ask:

- Is Discord already installed in OpenClaw?

### If yes

Only ask for:

- `DISCORD_VOICE_CHANNEL_ID`

### If no

Ask for:

- Discord plugin/integration
- `DISCORD_TOKEN`
- `DISCORD_VOICE_CHANNEL_ID`
- optional `DISCORD_GUILD_ID`

## 2. Detect model state

Ask:

- Do you want the default OpenClaw chat model first, or do you want to change it now?

### Default path

Use OpenClaw normal chat settings first.

### Custom path

Let the user set:

- `OPENCLAW_MODEL`
- `OPENCLAW_AGENT_ID`
- `OPENCLAW_REPLY_STRATEGY`

## 3. Confirm runtime readiness

Verify:

- bot can join voice
- `/status` works
- a short `/say` test works
- one real voice turn returns a short reply

## 4. Escalate only if needed

If something fails, ask for the next missing input instead of dumping the entire setup checklist again.
