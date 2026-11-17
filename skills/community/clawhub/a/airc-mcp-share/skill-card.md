## Description:

Use another agent's MCP tools remotely, or share your own MCP server with an agent on another machine or in another organisation, over the AIRC protocol (airc.dev).

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelskymonde](https://clawhub.ai/user/rafaelskymonde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to connect agents across machines so they can call selected MCP tools remotely. It guides users through importing a remote server or exporting a local server with explicit access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says a missing reference leaves the install review incomplete.

Mitigation: Review the installer and its referenced release source before running it; the installer downloads and installs the AIRC client.

Risk: An accepted link can let a remote agent call exported tools using the exporter's local privileges.

Mitigation: Require explicit user approval for links and exports, use a narrow --allow list, pin the exported server version, and share only a dedicated folder when exposing files.

Risk: Imported tools are code and results supplied by another party.

Mitigation: Treat imported tool results as untrusted and do not send secrets as tool arguments.

## Reference(s):

- [AIRC](https://airc.dev)
- [AIRC transport documentation](https://airc.dev/docs/transport)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
