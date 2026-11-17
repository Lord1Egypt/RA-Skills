## Description:

The Agency activates specialized professional roles, such as frontend developer, sales agent, or marketing specialist, when a user asks the agent to switch roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keda118228-dev](https://clawhub.ai/user/keda118228-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this meta-skill to activate domain-specific professional personas and workflows from the bundled role files. It is intended for role-guided responses, plans, code, configuration, analysis, and operational guidance across engineering, business, design, testing, and specialized domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad role switching can activate roles that publish content, move money, change production routing, persist memory, remediate data, or propose unsafe code.

Mitigation: Enable only required roles and require human approval, credential scoping, audit logs, data redaction, rollback planning, and environment isolation for high-impact actions.

Risk: Generated role guidance may be inaccurate or unsuitable for a specific business, legal, security, or production context.

Mitigation: Review outputs before execution, especially commands, code, payment actions, public publishing, and production changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keda118228-dev/skills/agency-agents-main)
- [ClawHub publisher profile](https://clawhub.ai/user/keda118228-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, configuration, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by activated role and should be reviewed before execution or operational use.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
