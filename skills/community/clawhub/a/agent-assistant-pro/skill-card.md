## Description:

Agent身份助手专业版 helps teams manage agent persona matrices, dynamic persona routing, compliance audits, persona A/B testing, version control, and team collaboration for enterprise agent identity governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, product teams, support leaders, and compliance reviewers use this skill to define, route, audit, test, version, and share agent personas across business lines, brands, user segments, and regulated scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read, write, and command execution capabilities for persona management workflows.

Mitigation: Install it only in workspaces where persona files and related commands may be managed, and require explicit approval before writes, migrations, exports, routing changes, or command execution.

Risk: Credential and external integration guidance is under-scoped, including tokens, callbacks, CRM/CDP integrations, and private deployment credentials.

Mitigation: Use environment variables or a secret manager for tokens, avoid hardcoded secrets, keep callbacks disabled unless required, and review external endpoints before use.

Risk: Persona routing, compliance audit, and A/B testing outputs can affect agent behavior in business or regulated workflows.

Mitigation: Review generated persona, routing, audit, and test configurations with the responsible business or compliance owner before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agent-assistant-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persona definitions, routing rules, audit outputs, migration steps, exports, callbacks, and command execution steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
