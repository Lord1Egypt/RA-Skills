## Description:

A 3-tier decision framework that defines when your AI agent should act independently, report with detail, or ask before proceeding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to define agent autonomy tiers for routine, auditable, and approval-gated actions in operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomy tiers could let an agent act without prior approval on production, financial, credential, infrastructure, repository-write, or customer-facing work.

Mitigation: Narrow the tiers to the deployment environment and keep those high-impact action categories approval-gated unless explicitly reviewed and approved.

Risk: Persistent MEMORY.md, SOUL.md, or HEARTBEAT.md changes could make agent behavior more autonomous than intended.

Mitigation: Approve the exact policy text before persistence and keep a rollback path for reverting autonomy policy changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeytbuilds/skills/autonomy-ladder)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with reusable policy snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested MEMORY.md, SOUL.md, and HEARTBEAT.md text for agent autonomy policy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
