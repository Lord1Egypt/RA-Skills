## Description:

Creates and configures a new OpenClaw agent workspace, including memory files, OpenClaw configuration, Feishu channel setup, bindings, and multi-agent collaboration settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add OpenClaw agents, create their workspace and memory structure, update openclaw.json, connect a Feishu bot account, and restart the OpenClaw gateway so the agent can receive messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad cross-agent access through subagents.allowAgents ["*"].

Mitigation: Replace the wildcard with an empty list or a narrow allowlist unless broad multi-agent spawning is explicitly required.

Risk: Feishu appSecret values may be stored in openclaw.json.

Mitigation: Protect the configuration file and avoid exposing the appSecret in shared logs, repositories, or screenshots.

Risk: Private agents may become reachable through Feishu if channel policies are too open.

Mitigation: Use pairing or allowlist policies for direct messages and groups, and verify bindings before restarting the gateway.

## Reference(s):

- [Openclaw Create Agent skill page](https://clawhub.ai/caoyachao/skills/create-agent-feishu)
- [Feishu Open Platform app console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create OpenClaw workspace files and directories, modify openclaw.json, and instruct a gateway restart.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
