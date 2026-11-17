## Description:

Feishu/Lark bot operations runbook for diagnosing and fixing deployment, messaging, @mention, bot-to-bot communication, session context, WebSocket, authentication, and interactive-card callback issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femi-ronvue](https://clawhub.ai/user/femi-ronvue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot and recover Hermes Agent integrations with Feishu/Lark bots. It provides diagnostic workflows, configuration guidance, API checks, patch guidance, and recovery commands for common bot operations incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands and guidance that can change .env/config settings, stop processes, remove lock files, and alter persistent bot visibility behavior.

Mitigation: Require human approval before applying configuration changes or process-control commands, and back up configuration before persistent changes.

Risk: Broad access settings such as GATEWAY_ALLOW_ALL_USERS can bypass normal user filtering during diagnostics.

Mitigation: Use broad access only in tightly controlled temporary diagnostics, then restore the intended allowlist or group policy.

Risk: The recovery script installs lark-oapi and restarts gateway processes, which can affect runtime availability and dependency state.

Mitigation: Pin lark-oapi where possible, verify target gateway PIDs before stopping them, and confirm Feishu connection after restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/femi-ronvue/skills/feishu-bot-ops)
- [AT_MAP code patch reference](references/at-mention-code-fix.md)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Lark tenant access token API](https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages/<message_id>)
- [Feishu chat members API](https://open.feishu.cn/open-apis/im/v1/chats/<chat_id>/members)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands, configuration snippets, API request examples, and patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are operational recommendations for human review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
