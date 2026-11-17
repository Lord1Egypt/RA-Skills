## Description:

Interact with remote CLI, API, and MCP tools via the CogenticLink CLI, using progressive disclosure from tool library to category to tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cogenticlab](https://clawhub.ai/user/cogenticlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure CogenticLink tool-library tokens, browse available remote tool categories and tools, inspect tool schemas, and execute tool calls through CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run the CogenticLink CLI without pinning a trusted package version.

Mitigation: Install only a trusted, pinned CogenticLink version and review the package source or provenance before deployment.

Risk: API tokens may be exposed through shared terminals, shell history, logs, or weak local configuration protection.

Mitigation: Use narrowly scoped revocable tokens, avoid entering real tokens in shared command contexts, and verify permissions on ~/.cogenticlab/link/config.json.

Risk: Remote tool calls can execute against external tool libraries using user-provided credentials.

Mitigation: Review tool descriptions and input schemas before each call, and prefer least-privilege libraries for sensitive workflows.

## Reference(s):

- [Connect Tool Library on ClawHub](https://clawhub.ai/cogenticlab/skills/connect-tool-library)
- [CogenticLink npm package](https://www.npmjs.com/package/cogenticlink)
- [cogenticlab publisher profile](https://clawhub.ai/user/cogenticlab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local CogenticLink configuration and to call remote tools with user-provided tokens.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
