## Description:

Answers AgentBox Cloud sandbox setup and usage questions using the official AgentBox docs summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoygang](https://clawhub.ai/user/guoygang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer common AgentBox sandbox questions about quickstart setup, CLI authentication, Python SDK usage, sandbox lifecycle, commands, filesystem access, environment variables, and custom templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential examples could be copied with real passwords or API keys.

Mitigation: Use interactive login, environment variables, or a secret manager, and keep secrets scoped to individual commands or runs when possible.

Risk: The bundled documentation summary may not cover every current AgentBox feature or auth flow.

Mitigation: For behavior not covered by the bundled reference, check the latest official AgentBox documentation before acting.

## Reference(s):

- [AgentBox official docs summary](references/agentbox-official.md)
- [AgentBox documentation](https://agentbox.cloud/docs)
- [AgentBox homepage](https://agentbox.cloud/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only AgentBox documentation guidance; examples may include placeholder API keys, environment variables, CLI commands, and Python SDK snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
