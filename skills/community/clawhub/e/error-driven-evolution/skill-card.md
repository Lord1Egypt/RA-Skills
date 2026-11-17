## Description:

Structured error-to-rule learning system for AI agents that converts mistakes and user corrections into executable rules in lessons.md, scans those rules before future decisions, and supports anonymized community sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marsnavi](https://clawhub.ai/user/marsnavi)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to turn corrections and repeated mistakes into durable behavioral rules that agents scan before future decisions. It is intended for workspace-level agent behavior improvement and optional anonymized sharing of reusable lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace-level rules can influence later agent decisions and may capture sensitive or project-specific details if saved without review.

Mitigation: Review every new lesson before saving it, avoid secrets and sensitive project details, and periodically retire obsolete or overly broad rules.

Risk: Community rule files can introduce unvalidated or unsuitable guidance into an agent workflow.

Mitigation: Pin or manually review community rule files before use, and treat imported lessons as guidance that must be checked against the current task context.

## Reference(s):

- [Community Sharing](references/community-sharing.md)
- [Quick Reference](references/quick-ref.md)
- [Agent Lessons Community Repository](https://github.com/anthropic-ai/agent-lessons)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace-level lesson rules and optional anonymized community submissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
