## Description:

Feishu CLI Chat helps agents use feishu-cli to browse Feishu chat history, search conversations, inspect message details, add reactions, pin or delete messages, and manage group chat information and members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giswilson](https://clawhub.ai/user/giswilson)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and authorized operators use this skill when they need an agent to retrieve and summarize Feishu chat or group history, search conversations, inspect message details, and perform scoped group or message management with a logged-in user token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private Feishu chat and group history through broad user-level access.

Mitigation: Install only for authorized Feishu workspaces and accounts, use the narrowest practical Feishu scopes, and avoid accessing third-party private conversations without clear authorization.

Risk: The skill supports high-impact group and message actions such as member changes, pinning, deletion, and group dissolution.

Mitigation: Require manual review before executing management actions that alter membership, message state, or group availability.

## Reference(s):

- [Feishu Cli Chat on ClawHub](https://clawhub.ai/giswilson/skills/feishu-cli-chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Feishu user token for the main read and management workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
