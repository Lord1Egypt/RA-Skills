## Description:

Mirrors messages sent by OpenClaw command crons or scripts into the owning agent's session transcript so the agent retains a durable record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obuchowski](https://clawhub.ai/user/obuchowski)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who run OpenClaw command crons, dispatcher jobs, reminder scripts, or status checkers use this skill to send channel messages and mirror the delivered text into the owning agent's transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback session matching can persist delivered content in the wrong transcript when chat IDs or sessions overlap.

Mitigation: Prefer explicit session keys or exact agent, channel, target, and thread values; review or patch fallback matching before use in multi-session environments.

Risk: Untrusted cron or script input is sent and stored verbatim in transcript history.

Mitigation: Invoke the helper only from trusted callers and validate message sources before passing content into the skill.

Risk: Concurrent transcript writes can interleave with live gateway appends.

Mitigation: Use it for dispatcher schedules when the target agent is idle, keep per-session advisory locking enabled, and re-verify behavior after major OpenClaw upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/cron-to-transcript)
- [Project homepage](https://github.com/obuchowski/openclaw-cron-to-transcript)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw message-send commands and transcript-mirroring guidance; runtime helper can append JSONL transcript records and idempotency state.]

## Skill Version(s):

1.0.2 (source: server release metadata and CHANGELOG, released 2026-06-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
