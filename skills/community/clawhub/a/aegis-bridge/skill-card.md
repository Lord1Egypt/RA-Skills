## Description:

Aegis Bridge helps agents orchestrate local Claude Code sessions through an Aegis HTTP/MCP bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onestepat4time](https://clawhub.ai/user/onestepat4time)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create, supervise, inspect, and clean up Claude Code sessions for implementation, review, CI repair, and parallel coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended approval of coding-agent permissions can allow unwanted tool use or shell actions.

Mitigation: Use manual review, explicit allowlists, audit logging, and isolated environments before enabling auto-approval workflows.

Risk: The MCP setup can install a persistent unpinned aegis-bridge command through npx.

Mitigation: Prefer project-scoped MCP configuration and pin or locally verify the aegis-bridge executable before use.

Risk: Prompts, transcripts, raw terminal output, and approval requests may contain sensitive project information.

Mitigation: Treat session data as sensitive and restrict access to workspaces, logs, and transcript outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onestepat4time/skills/aegis-bridge)
- [Aegis API Quick Reference](references/api-quick-ref.md)
- [Agent Template](references/agent-template.md)
- [Heartbeat Template](references/heartbeat-template.md)
- [Workflow Examples](references/workflow-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTTP examples, MCP tool names, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Aegis server on localhost:9100, Node.js 20+, Claude Code CLI, and jq for helper scripts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
