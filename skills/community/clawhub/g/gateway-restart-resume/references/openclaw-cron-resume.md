# OpenClaw Cron Resume Pattern

Use this only when the durable callback is an OpenClaw cron job. Confirm flags against `openclaw cron add --help` on the installed OpenClaw version.

## One-Shot Callback

Create the callback before restarting:

```bash
openclaw cron add \
  --name "gateway-restart-resume-<timestamp>" \
  --at +90s \
  --agent <agent-id> \
  --session isolated \
  --light-context \
  --tools gateway,message,exec \
  --announce \
  --account <account-id-if-needed> \
  --channel <original-channel-or-last> \
  --to <original-addressable-target-if-needed> \
  --delete-after-run \
  --timeout-seconds 120 \
  --message '<compact resume instruction with sanitized routing payload>'
```

The message should tell the agent to:

1. Check gateway/service status and health.
2. Check the original medium delivery path when supported.
3. Reply to the captured target with the operator report format from `SKILL.md`.
4. If the gateway is still unavailable, reschedule one one-shot retry and increment an `attempt` field.
5. Stop after 3 total attempts or about 5 minutes and leave a durable failure note.

## Payload Rules

- Include only routing metadata needed for the reply.
- Do not include raw user text, transcripts, secrets, env values, tokens, or full config.
- Do not create a repeating cron for a restart resume unless an operator explicitly asks for monitoring.
- For Discord or Slack threads, use the installed OpenClaw version's routable conversation/channel target. Do not use flags that are documented for another channel type.
