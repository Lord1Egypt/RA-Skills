## Description:

Commitment Engine turns time-bound verbal tasks into trackable commitment records with heartbeat checks and optional OpenClaw cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dottythehomeless](https://clawhub.ai/user/dottythehomeless)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an assistant record, track, prepare, and escalate time-bound commitments instead of relying on conversational memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create durable commitment records and scheduled OpenClaw cron jobs that persist beyond the original conversation.

Mitigation: Require explicit confirmation before any cron job is created, review the schedule and message, and maintain clear list, cancel, expire, and cleanup procedures.

Risk: Priority interruption and overdue escalation can disrupt other agent work if commitments are recorded incorrectly or left stale.

Mitigation: Review commitment entries before activation and regularly expire, complete, or cancel stale records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dottythehomeless/skills/commitment-engine)
- [Publisher profile](https://clawhub.ai/user/dottythehomeless)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown ledger entries, OpenClaw cron commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create durable commitment records and scheduled jobs when adopted by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
