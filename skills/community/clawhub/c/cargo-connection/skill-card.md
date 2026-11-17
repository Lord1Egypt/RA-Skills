## Description:

Manage Cargo connectors and integrations, including discovery, authentication, and connection maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover integrations, inspect available actions, and manage authenticated Cargo connections for their workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing a connector may affect dependent workflows, tools, or models.

Mitigation: Review an impact list and get approval before deletion; prefer moving dependent connections where suitable.

Risk: Connector configuration and CLI output may expose credentials.

Mitigation: Use narrowly scoped credentials and protect CLI output that contains connector configuration.

Risk: The external CLI and companion safety documentation were not verified.

Mitigation: Review the CLI version and relevant safety documentation before use, and pin a reviewed CLI version.

## Reference(s):

- [Connector examples](artifact/references/examples/connectors.md)
- [Integration examples](artifact/references/examples/integrations.md)
- [Response shapes](artifact/references/response-shapes.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Cargo skills repository homepage](https://github.com/getcargohq/cargo-skills)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON response examples, Operational guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.7.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
