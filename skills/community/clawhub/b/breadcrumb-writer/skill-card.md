## Description:

Guides agents to keep HEARTBEAT.md updates brief, single-entry, replacement-only, and no more frequent than once per hour.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quratus](https://clawhub.ai/user/quratus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a repository relies on HEARTBEAT.md for coordination and they need agents to write one concise status block without clutter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill in projects that do not use HEARTBEAT.md can create irrelevant coordination guidance.

Mitigation: Confirm the project uses HEARTBEAT.md for task coordination before installing or invoking the skill.

Risk: Frequent or append-only updates can clutter HEARTBEAT.md and confuse coordination.

Mitigation: Replace the file with one short block and skip updates if HEARTBEAT.md changed within the last 60 minutes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quratus/skills/breadcrumb-writer)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Concise Markdown status guidance for HEARTBEAT.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replacement-only status block; avoid repeated sections and skip updates if HEARTBEAT.md changed within the last 60 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
