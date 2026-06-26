---
name: gateway-restart-resume
description: Use when an OpenClaw gateway-backed agent is asked through Discord, Slack, Matrix, SMS, web chat, CLI relay, ACP, cron, or another channel to restart, stop, reload, update, or repair the gateway and needs a durable post-restart callback, same-thread reply, recovery status, or lost follow-up prevention.
---

# OpenClaw Restart Resume

## Overview

Gateway restart is a conversation-continuity problem. An in-gateway OpenClaw agent that restarts the gateway kills the runtime that would normally send the follow-up reply. Before taking any gateway-killing action, create a durable resume path that can verify recovery and report back through the same medium, conversation, channel, thread, or user route.

## Runtime Tool Preflight

Before any in-gateway restart attempt, verify that the current runtime exposes a durable control path:

- `cron` or an equivalent durable task tool for the resume callback.
- `gateway` or `exec` for the restart action.
- A delivery path for the original medium, such as cron `announce` delivery, the original session route, or an approved channel send mechanism.

If any required path is unavailable, do not restart. Reply in the current conversation with a short degraded status:

```text
I did not restart the gateway because this runtime cannot create a durable post-restart callback first.
Needed before retry: cron/task callback access plus gateway/exec restart access.
```

Never replace this preflight with best-effort memory, a note in the transcript, or an instruction to yourself. The callback must be durable outside the current in-gateway turn.

## Pre-Restart Gate

Before any restart, explicitly satisfy every item:

- Durable callback created outside the current in-gateway turn.
- Original reply route captured with no secrets or raw message bodies.
- Short pre-restart acknowledgement sent to the user.
- Restart action explicitly requested or approved.
- Callback includes verification steps, bounded retry budget, and failure reporting.

If any item is missing, do not restart. Report the missing prerequisite in the current conversation.

## When to Use

Use this skill when:

- A user asks through Discord, Slack, Matrix, SMS, email, web chat, CLI relay, ACP, cron, or another OpenClaw-backed medium to restart, stop, reload, update, or repair the gateway.
- The action may stop the gateway, restart the service manager, reload plugins, or replace the running OpenClaw package.
- The agent is running inside OpenClaw, or may be running inside OpenClaw.
- The user expects a post-restart status reply.

Do not use this skill for external shell operators that can survive the restart themselves, except as a checklist for user-facing notifications.

## Restart Resume Protocol

1. Classify execution context.
   - If running inside OpenClaw, assume the restart will terminate the current turn.
   - If running outside OpenClaw, still use the notification and verification steps when the request came from a user-facing channel.

2. Confirm permission.
   - If the user did not explicitly ask for restart/stop/update, ask first.
   - Do not restart for vague requests such as "fix it" until the restart is explained and approved.

3. Capture reply target.
   - Record the medium, account/profile if relevant, conversation id, channel id, thread id, message id, user id if needed, and agent id.
   - Prefer the exact original route. If the medium has no thread concept, record the smallest addressable conversation target.
   - Store only routing metadata needed to reply. Do not store raw message bodies, tokens, env contents, or secrets.

4. Send pre-restart acknowledgement.
   - Tell the user the gateway is restarting and that a follow-up will be sent after verification.
   - Keep it short because the gateway may stop immediately afterward.

5. Create durable resume callback before restart.
   - Prefer a one-shot or short-delay OpenClaw cron job, task, or native gateway callback that survives the gateway restart.
   - The callback must include the reply target and verification checklist.
   - If callback creation fails, do not restart. Tell the user the restart was not attempted because no follow-up path exists.
   - For OpenClaw cron, prefer a one-shot job with delete-after-run enabled and fallback delivery/announce pointed at the original medium target.
   - For cron-specific command shape, read [references/openclaw-cron-resume.md](references/openclaw-cron-resume.md) only when using OpenClaw cron.

6. Restart only after the callback exists.
   - Use the narrowest approved restart action.
   - Avoid broad update/reinstall operations unless the user requested them and the current admin runbook supports them.

7. Resume callback verifies recovery.
   - Check gateway/service status.
   - Check health endpoint or gateway probe.
   - Check connectivity or send capability for the original medium when the local OpenClaw version supports it.
   - Check plugin or task health only when relevant to the restart reason.

8. Send final reply.
   - Reply in the original medium and conversation/thread when available.
   - Use the operator report format below unless the original medium requires a shorter message.
   - State whether restart completed, what was verified, duration if known, and any remaining warning.
   - If verification fails, report the failed check and the safest next action.
   - Translate raw tool results into human status. Never paste raw strings such as `gateway.restart`, `restart ok`, `restart restart ok`, method names, JSON payloads, or internal reason text into the user-facing reply.

## Medium-Agnostic Reply Rules

- Discord/Slack/Matrix: reply in the original thread when available; otherwise reply in the original channel/conversation.
- SMS/chat apps: keep the final message compact and avoid multi-line technical detail unless the user asked for it.
- Email: include a concise subject-like first line, then the verification report.
- CLI relay or ACP: return structured status when the caller expects JSON/tool output; include human-readable summary when routed to a person.
- Cron or automation-triggered restarts: send the final report to the configured notification target and record the result in durable run history if available.
- If the original medium is unavailable after restart, use the configured fallback notification target only when policy allows it; otherwise leave a durable ops note for the operator.

## Resume Payload

The durable callback should carry a minimal payload:

```json
{
  "reason": "user-requested gateway restart",
  "agentId": "<agent-id>",
  "reply": {
    "medium": "<discord|slack|matrix|sms|email|web|cli|acp|cron|other>",
    "account": "<account-id-if-needed>",
    "target": "<conversation-or-addressable-target>",
    "channelId": "<channel-id-if-needed>",
    "threadId": "<thread-id-if-needed>",
    "userId": "<user-id-if-needed>",
    "messageId": "<original-message-id-if-needed>"
  },
  "verify": [
    "gateway status",
    "health",
    "original medium connectivity"
  ],
  "createdAt": "<iso-timestamp>"
}
```

Sanitize or omit fields that are not needed for routing. Never include secrets, full config, env files, transcript bodies, or private message contents.

## Verification Checklist

Use the local OpenClaw version's native tools when available. Equivalent checks are acceptable.

```bash
openclaw gateway status
openclaw health
openclaw channels status --probe
```

When the restart was part of an update or plugin repair, also verify the relevant narrow checks, for example:

```bash
openclaw doctor --non-interactive --no-workspace-suggestions
openclaw plugins doctor
openclaw tasks audit
```

Do not claim the restart succeeded unless fresh verification output supports it.

## Failure Handling

- Callback creation fails: do not restart; explain that there is no durable way to report back.
- Restart command fails before shutdown: report the command failure immediately in the current medium.
- Gateway returns but the original medium is disconnected: report through any still-available approved fallback route, or leave a durable task/ops note for the operator.
- Gateway does not return: retry verification up to 3 total attempts over about 5 minutes, then record the failure in durable state and stop.
- Auth/token errors appear: do not read or paste secrets. Report the config path/key names only and ask for explicit operator direction.

## Common Mistakes

- Restarting first and trying to schedule the follow-up afterward.
- Treating "gateway command returned" as proof that the original medium recovered.
- Storing raw messages or secret-bearing config in the resume payload.
- Creating a repeating cron when a one-shot callback is enough.
- Retrying forever after a failed restart.
- Sending the final reply to a default destination instead of the original medium/conversation/thread.

## Output Message Format

Prefer this operator report for human-facing media that can handle multi-line messages.

Output must be written as a clean operator status, not as a tool transcript.

Do not include:

- Raw tool names or method names, such as `gateway.restart`.
- Duplicated/generated phrases, such as "restart restart ok".
- Internal reason payloads unless the user explicitly asks for them.
- "Recommended follow-up: run openclaw doctor..." after a successful restart. Only suggest a terminal command when verification failed or is genuinely blocked.

Before restart:

```text
Restarting the OpenClaw gateway now.
I will reply here after it comes back.
```

After success:

```text
Gateway restart complete.

Verified:
- Gateway: back online
- Discord: reply path restored
- Resume: this follow-up reached the original thread

Duration: <duration or "not recorded">
Warnings: <none or one short warning>
```

After degraded recovery:

```text
Gateway restart completed, but verification is degraded.

Passed:
- <passed check>

Needs attention:
- <failed or warning check>

Safest next action: <next step>.
```

After failure:

```text
Gateway restart did not verify cleanly.

Failed check: <check>
Last known state: <state>
Safest next action: <next step>
```
