## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can log session outcomes and promote broadly applicable guidance into persistent instruction files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinuscxj](https://clawhub.ai/user/dinuscxj)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to record command failures, user corrections, missing capabilities, outdated knowledge, and recurring practices. It also provides optional hook setup guidance for reminding agents to capture and promote high-value learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages retaining session-derived content in persistent learning logs, which can capture secrets, personal data, or sensitive project details.

Mitigation: Redact secrets and personal data before writing logs, and keep learning files project-local unless they have been reviewed for sharing.

Risk: Always-on hooks can repeatedly inject reminders or inspect command output in ways that affect agent context and workflow behavior.

Mitigation: Enable hooks explicitly, keep them project-local, avoid broad empty matchers where possible, and review hook scripts before activation.

Risk: Promoting learnings into persistent instruction files can preserve incorrect, misleading, or overly broad guidance.

Mitigation: Require human review before promotion and keep promoted rules concise, evidence-based, and scoped to the relevant project or agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinuscxj/skills/analyzing-business-strategy-skill-main)
- [OpenClaw integration guide](artifact/references/openclaw-integration.md)
- [Hook setup guide](artifact/references/hooks-setup.md)
- [Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, hook code, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning log entries and optional reminders; users should review entries before promoting them into instruction files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
