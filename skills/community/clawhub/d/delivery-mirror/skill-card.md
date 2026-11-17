## Description:

Mirror cron/script deliveries into agent session transcripts so scheduled and isolated-cron messages persist in context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obuchowski](https://clawhub.ai/user/obuchowski)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to send OpenClaw cron or script messages and mirror the delivered text into the owning agent's transcript so scheduled deliveries remain visible in later context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback session matching can write a caller-supplied message into the wrong persistent agent session.

Mitigation: Use explicit --session-key where possible, avoid fallback session discovery, and require exact normalized destination matches with rejection of multiple matches before use in shared or sensitive OpenClaw environments.

Risk: Caller-provided message content is stored verbatim in the target transcript.

Mitigation: Invoke the helper only from trusted cron jobs or scripts with trusted message content.

Risk: Mirroring into an actively running session can race with other writers.

Mitigation: Use the helper for dispatcher-style schedules when the agent is idle and avoid mirroring into a topic while its agent is mid-run.

## Reference(s):

- [Project homepage](https://github.com/obuchowski/openclaw-delivery-mirror)
- [ClawHub skill page](https://clawhub.ai/obuchowski/skills/delivery-mirror)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-line usage guidance for a Bash helper that sends messages, appends transcript JSONL rows, and records optional idempotency state.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and CHANGELOG, released 2026-06-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
