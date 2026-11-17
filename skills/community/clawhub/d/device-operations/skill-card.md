## Description:

Device Operations helps agents automate Android device control, social app workflows, multi-platform publishing, AutoGLM visual analysis, rule routing, self-learning records, and multi-device scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide device and social-account automation workflows, including Android actions, WeChat and marketplace messaging, short-form video publishing, visual UI analysis, rule optimization, and multi-device task coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP server may control Android devices and social accounts.

Mitigation: Inspect the MCP server implementation and configuration before installation, and restrict use to test devices or limited accounts unless the operator has approved broader access.

Risk: Automation can send messages, publish content, install apps, receive funds, or take screenshots.

Mitigation: Require explicit human confirmation before these actions and review task parameters before execution.

Risk: Screenshots, cookies, account data, and self-learning records may contain sensitive information.

Mitigation: Define where these records are stored, who can access them, and how they are deleted before enabling the skill.

## Reference(s):

- [Device operations reference data](artifact/scripts/device_operations_reference.json)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/device-operations)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Python, SILICONFLOW_API_KEY, and mcp.servers.device-operations-mcp configuration requirements.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
