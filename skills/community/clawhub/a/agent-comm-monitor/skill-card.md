## Description:

Monitors communication between muzhe and named agents, verifies one-way and two-way message delivery, and reports communication status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nancliu](https://clawhub.ai/user/nancliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check whether muzhe can communicate with named agents, inspect delivery status, and receive a concise status report when communication appears delayed or failed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect named agents' communication state and session history.

Mitigation: Limit checks to the named target agents and the current communication test window, and review the skill before installing where cross-agent history is sensitive.

Risk: The skill may write persistent abnormality logs to MEMORY.md or HEARTBEAT.md without clear user approval.

Mitigation: Ask before writing persistent logs, keep log contents minimal, and document what was written for user review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nancliu/skills/agent-comm-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status report with a concise table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include communication status, response timing, timeout notes, and follow-up guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
