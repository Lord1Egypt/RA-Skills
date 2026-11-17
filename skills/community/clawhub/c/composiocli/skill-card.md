## Description:

Use 1000+ external apps via Composio - either directly through the CLI or by building AI agents and apps with the SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eladrave](https://clawhub.ai/user/eladrave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search, connect, and execute Composio tools from the CLI, or to build AI agents and applications that integrate with external services through the Composio SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include a pipe-to-shell installer.

Mitigation: Review the installer first or replace it with a verified package or signed release before installation.

Risk: The skill can guide agents to perform high-impact actions in external accounts, including sending messages, posting content, creating issues, deleting connections, or changing trigger state.

Mitigation: Require explicit user confirmation before executing actions that change external account state.

Risk: Tool arguments and trigger payloads may contain sensitive user or account data.

Mitigation: Avoid logging full tool arguments or trigger payloads, and redact sensitive values when diagnostics are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eladrave/skills/composiocli)
- [Composio documentation](https://docs.composio.dev)
- [Composio platform](https://platform.composio.dev)
- [Composio CLI guide](rules/composio-cli.md)
- [Building with Composio](rules/building-with-composio.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
