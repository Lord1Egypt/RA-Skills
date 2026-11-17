## Description:

Redirect: conversation-recovery has been merged into context-preserver. Use context-preserver for session snapshots, recovery, task handoff, context export, and long-running work continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this redirect skill when older conversation-recovery references appear in a workflow and should be routed to context-preserver for session snapshots, recovery, handoff, context export, and long-running work continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session snapshots or handoff notes may include sensitive project details if copied without review.

Mitigation: Review snapshot contents before saving or sharing and omit unnecessary sensitive details.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with plain-text handoff and snapshot template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redirect-only guidance; does not execute code, call external services, or handle credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
