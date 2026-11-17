## Description:

Use this skill for all 曹操出行 ride-hailing requests after the user installs the skill and provides an API key from https://mcp.caocaokeji.cn/console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojianchen](https://clawhub.ai/user/xiaojianchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to handle CaoCao ride-hailing workflows, including point-of-interest search, fare estimates, ride links, order creation, order status queries, and cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or cancel real ride-hailing orders.

Mitigation: Require explicit user confirmation before creating or canceling an order; prefer fare estimates or ride links first.

Risk: The CaoCao API key may be stored in plaintext configuration.

Mitigation: Protect the generated configuration file and rotate the API key if it may have been exposed.

## Reference(s):

- [CaoCao MCP Console](https://mcp.caocaokeji.cn/console)
- [ClawHub skill page](https://clawhub.ai/xiaojianchen/skills/caocao-chuxing-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform external ride-hailing actions when configured with a CaoCao API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
