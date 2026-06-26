# OpenClaw Restart Resume

`gateway-restart-resume` is a small OpenClaw skill for one practical failure mode: an agent is asked to restart the gateway, but the restart kills the same runtime that would normally send the follow-up reply.

The skill gives agents a safe protocol:

1. Acknowledge the restart request in the original medium.
2. Capture only the routing metadata needed to reply later.
3. Create a durable resume callback before restarting.
4. Restart the gateway only after the callback exists.
5. Verify gateway, health, and original medium recovery.
6. Send a structured post-restart status report back to the original conversation.

## Use Case

Use this when OpenClaw is controlled from Discord, Slack, Matrix, SMS, email, web chat, CLI relay, ACP, cron, or another gateway-backed medium and the user expects an answer after the gateway comes back.

Without this protocol, an in-gateway agent can truthfully start a restart but never return to say whether the restart worked.

## Current Behavior

- Requires a durable callback path before restart: `cron` or equivalent task scheduling.
- Requires a restart path: native gateway restart tool or approved shell execution.
- Requires a delivery route back to the original medium, channel, thread, or conversation.
- Requires a hard pre-restart gate: callback created, route captured, acknowledgement sent, restart approved, and retry/failure reporting defined.
- Refuses to restart if the callback path cannot be created first.
- Keeps the resume payload minimal: routing metadata and verification checks only.
- Bounds failed recovery retries to 3 total attempts over about 5 minutes.
- Produces a clean human status message after restart instead of raw tool output.

Successful post-restart replies should look like:

```text
Gateway restart complete.

Verified:
- Gateway: back online
- Discord: reply path restored
- Resume: this follow-up reached the original thread

Duration: not recorded
Warnings: none
```

The skill explicitly tells agents not to paste raw tool strings such as `gateway.restart`, duplicated phrases like `restart restart ok`, JSON payloads, internal reason text, or terminal follow-up recommendations after a successful restart.

## Install

```bash
clawhub install gateway-restart-resume
```

ClawHub:

```text
https://clawhub.ai/udaymanish6/gateway-restart-resume
```

GitHub:

```text
https://github.com/udaymanish6/openclaw-restart-resume
```

## What It Does Not Do

- It does not restart OpenClaw by itself.
- It does not read secrets or env files.
- It does not replace an OpenClaw admin/update runbook.
- It does not assume Discord; Discord is only one supported medium.

## Community

If this solves a real restart-follow-up problem in your OpenClaw setup, please star it on ClawHub or GitHub so other operators can find it.
