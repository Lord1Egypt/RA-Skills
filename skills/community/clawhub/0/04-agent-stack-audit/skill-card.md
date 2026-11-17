## Description:

Monthly health check for an agent stack that inspects scheduled tasks, scripts, API usage, skills, memory files, tools, and subscriptions, then classifies findings into a ranked cleanup brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingukim225](https://clawhub.ai/user/pingukim225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit automation stacks for stale jobs, unused services, duplicate tools, and outdated local context before deciding what to remove, merge, or upgrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive local operational context, including scheduled tasks, local scripts, API configuration, installed skills, and memory or context files.

Mitigation: Run it only with explicit directory and data-category boundaries, and redact secrets or private project context from generated reports.

Risk: Cleanup recommendations may affect active automations if acted on without review.

Mitigation: Treat findings as recommendations, require explicit user approval before deletion, and classify uncertain items as needing user input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pingukim225/skills/04-agent-stack-audit)
- [Publisher Profile](https://clawhub.ai/user/pingukim225)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with ranked findings, tables, recommended actions, and optional shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed cleanup actions for user review and may write dated audit or cleanup reports under state/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
