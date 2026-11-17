## Description:

Connect to AgentMailer's hosted MCP server, complete human-approved OAuth, or troubleshoot authentication in Claude Code, Codex, Cursor, and other MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure AgentMailer's remote MCP server, complete human-approved OAuth, verify permissions, and troubleshoot connection or authorization failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent remote MCP configuration and OAuth authorization flow can grant access to AgentMailer operations.

Mitigation: Install only when you intend to connect to AgentMailer, complete human approval, and review auth_me permissions before creating inboxes or enabling direct agent communication.

Risk: Creating inboxes or using direct agent communication with an untrusted or insufficiently scoped credential could fail or expose unintended capabilities.

Mitigation: Require auth_me to report a trusted identity and the needed inboxes:create or a2a permissions before attempting those operations.

Risk: Connection diagnostics could expose access tokens, authorization headers, approval codes, or reviewer credentials.

Mitigation: Follow the troubleshooting guidance and keep secrets out of prompts, source files, shell history, and diagnostic output.

## Reference(s):

- [AgentMailer MCP ClawHub page](https://clawhub.ai/agentmailer/skills/agentmailer-mcp)
- [MCP troubleshooting](references/troubleshooting.md)
- [AgentMailer MCP endpoint](https://api.agentmailer.ai/mcp)
- [AgentMailer authentication guide](https://api.agentmailer.ai/auth.md)
- [AgentMailer documentation](https://agentmailer.ai/docs)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)
- [Human-approved signup example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-human-approved-signup)
- [AgentMailer quickstart example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-quickstart)
- [AgentMailer CLI workflows](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on remote Streamable HTTP MCP setup, OAuth authorization, permission checks, and troubleshooting.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
