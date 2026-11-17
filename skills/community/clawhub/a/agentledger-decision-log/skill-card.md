## Description:

AI-powered decision journal for solopreneurs — capture decisions with context, rationale, and expected outcomes, then review them later to learn from what you got right and wrong.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

MIT-0

## Use Case:

Solopreneurs and small-business operators use this skill to have an agent capture significant business, product, financial, and strategy decisions as structured Markdown records. They can later review outcomes, identify decision patterns, and calibrate confidence over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision logs can contain sensitive business, financial, client, or personal context, especially if stored in synced or public repositories.

Mitigation: Choose the storage location before use, avoid sensitive details in shared repositories, and review generated entries before saving.

Risk: Optional automatic triggers for spending, project, or tool-adoption mentions may prompt logging more often than intended.

Mitigation: Narrow or skip automatic triggers and require confirmation before creating new decision entries.

Risk: Decision reviews and pattern summaries may be incomplete or misleading if based on sparse or vague entries.

Mitigation: Use concrete expected outcomes, scheduled review dates, and manual review of generated summaries before acting on them.

## Reference(s):

- [Decision Log - Advanced Patterns](references/advanced-patterns.md)
- [Decision Log on ClawHub](https://clawhub.ai/clawdssen/skills/agentledger-decision-log)
- [The Agent Ledger](https://theagentledger.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown templates and prompts with inline shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local decision-log Markdown files under a user-selected decisions/ directory.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
