## Description:

Guides a new user or agent through the initial setup, configuration, and capabilities of the Fulcra environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to connect a Fulcra account, learn Fulcra access options, and establish an initial project workflow with shared data, workspace coordination, and next-step skill handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned external Fulcra CLI while handling sensitive personal data and persistent credentials.

Mitigation: Review before installing, prefer a pinned and reviewed CLI version, and protect the Fulcra credentials file.

Risk: Fulcra onboarding can involve uploading local files, creating remote schemas, and working with personal data.

Mitigation: Confirm with the user before uploading files or creating schemas, and avoid unrelated secrets in the environment.

Risk: The release security verdict is suspicious despite no individual risk findings.

Mitigation: Use only in an environment where running the Fulcra CLI is acceptable and review the skill before deployment.

## Reference(s):

- [Fulcra CLI reference](references/fulcra-cli.md)
- [Fulcra website](https://www.fulcradynamics.com/)
- [Fulcra REST API documentation](https://fulcradynamics.github.io/developer-docs/api-reference/)
- [Fulcra Python SDK and CLI source](https://github.com/fulcradynamics/fulcra-api-python/)
- [Fulcra MCP documentation](https://fulcradynamics.github.io/developer-docs/mcp-server/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, URLs, and structured next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run the Fulcra CLI, authenticate the user, create schemas, upload files, and hand off to related Fulcra skills.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
