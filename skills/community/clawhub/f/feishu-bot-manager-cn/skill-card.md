## Description:

Manages Feishu bot accounts and routing bindings in OpenClaw, including account-level or group-level routes to existing agents and optional setup of a new agent workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-shen1121](https://clawhub.ai/user/alex-shen1121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add Feishu bot credentials, bind bot accounts or group chats to agents, and coordinate the required gateway restart and /feishu auth follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store Feishu App Secrets in OpenClaw configuration and backups.

Mitigation: Avoid pasting production secrets into chat or shell history, rotate any exposed secret, and review backup files for plaintext secrets.

Risk: The skill can broaden bot access through DM policy and route bindings.

Mitigation: Verify bot DM policy, allowlists, account-level bindings, and group-level bindings before enabling the account.

Risk: The skill can change global OpenClaw settings and restart the Gateway.

Mitigation: Use it only where the operator is authorized to modify OpenClaw configuration, review the generated changes, and confirm before restart.

## Reference(s):

- [New Agent Governance Rules](references/new-agent-governance.md)
- [Feishu OpenClaw Bot Creation Page](https://open.feishu.cn/page/openclaw?form=multiAgent)
- [ClawHub Skill Page](https://clawhub.ai/alex-shen1121/skills/feishu-bot-manager-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and file or configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration, initialize agent workspace files, create backups, and request operator confirmation before gateway restart.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
