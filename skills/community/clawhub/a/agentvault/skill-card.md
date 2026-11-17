## Description:

Encrypted credential vault and persistent memory for AI agents. Install from npm, sandbox agent access to secrets, store and query encrypted memory, run an MCP server, and audit every credential access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheen-sajjad](https://clawhub.ai/user/maheen-sajjad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Agentvault to manage encrypted local credentials and persistent memory for AI agents, configure sandboxed command execution, expose local MCP vault tools, and audit credential access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials, vault exports, memory exports, and audit data that may contain sensitive information.

Mitigation: Require explicit user confirmation for secret writes, imports, exports, audit clearing, memory writes, and vault operations; treat all exported vault, memory, and audit files as sensitive.

Risk: The install path uses npm or npx without a pinned package version.

Mitigation: Audit the package before installation and pin the intended @inflectiv-ai/agentvault version.

Risk: Autonomous persistent-memory reads can reveal stored local context.

Mitigation: Limit autonomous use to read-only queries only when appropriate, and require confirmation or disable autonomous memory queries for sensitive environments.

Risk: Weak passphrase choices or --skip-passphrase can weaken protection for real vault data.

Mitigation: Use a strong passphrase for real data and avoid --skip-passphrase outside development.

Risk: Passing private keys directly on the command line can expose them through shell history or process metadata.

Mitigation: Avoid command-line private key arguments; use safer secret import and storage workflows.

## Reference(s):

- [AgentVault Command Reference](references/commands.md)
- [AgentVault Documentation](https://agentvault.inflectiv.ai/documentation)
- [AgentVault Website](https://agentvault.inflectiv.ai)
- [npm Package](https://www.npmjs.com/package/@inflectiv-ai/agentvault)
- [AVP Specification](https://agentvaultprotocol.org/)
- [ClawHub Skill Page](https://clawhub.ai/maheen-sajjad/skills/agentvault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local CLI, MCP, vault, memory, and audit operations; write, export, install, and server-start actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
