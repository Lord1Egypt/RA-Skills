## Description:

Manage Feishu bots in OpenClaw configuration, including add, delete, update, list, and info operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangxinag-princess](https://clawhub.ai/user/xiangxinag-princess)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to manage Feishu bot accounts and their OpenClaw agent bindings from a shell workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets may be stored in plaintext OpenClaw configuration files, backups, or shell history.

Mitigation: Protect OpenClaw configuration and backup files, avoid exposing command history, and rotate secrets that may have been entered on the command line.

Risk: The generated Feishu account configuration allows broad access by default.

Mitigation: Restrict bot access policies and allowed senders after creation before using the bot in sensitive workspaces.

Risk: Untrusted or path-like bot identifiers can affect filesystem paths used for workspaces and agent directories.

Mitigation: Use only trusted simple bot identifiers until validation is added, and review paths before confirming directory deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiangxinag-princess/skills/feishu-bot-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/xiangxinag-princess)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and access to the user's OpenClaw configuration file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
