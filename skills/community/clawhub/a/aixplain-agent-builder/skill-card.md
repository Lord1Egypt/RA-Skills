## Description:

Design and deploy aiXplain agents with conservative defaults, read-only discovery first, and explicit approval gates for higher-risk actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nurhamdan1987](https://clawhub.ai/user/nurhamdan1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, inspect, build, deploy, and debug aiXplain agents while keeping marketplace searches, integrations, uploads, model choices, and write-capable actions behind explicit approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent creation, integrations, uploads, model changes, or write-capable tools can expand access or modify external systems.

Mitigation: Require explicit user approval for each higher-risk action and state exactly what will be created, changed, uploaded, or enabled before proceeding.

Risk: Debug traces may expose tool inputs, outputs, or model reasoning.

Mitigation: Use trace inspection only when needed for debugging or verification and warn users that detailed traces can include sensitive execution details.

Risk: Missing or ad hoc credentials can lead to insecure setup behavior.

Mitigation: Prefer existing environment configuration, stop when required variables such as AIXPLAIN_API_KEY are missing, and avoid requesting secrets in chat.

## Reference(s):

- [Safety Gates](references/safety-gates.md)
- [Read-Only Patterns](references/read-only-patterns.md)
- [aiXplain Agent Builder on ClawHub](https://clawhub.ai/nurhamdan1987/skills/aixplain-agent-builder)
- [Nur Hamdan ClawHub Profile](https://clawhub.ai/user/nurhamdan1987)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include aiXplain Studio links, OAuth redirect URLs, setup checks, execution traces, and approval prompts.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
