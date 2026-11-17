## Description:

飞书增强套件 helps Chinese-language users automate Feishu document, Bitable, messaging, and calendar workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijie298](https://clawhub.ai/user/lijie298)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and office automation users use this skill to configure Feishu app access, create or update Feishu content, batch-create Bitable records, send messages, and support calendar-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Feishu App ID and App Secret credentials.

Mitigation: Use a dedicated least-privilege Feishu app and store credentials in environment variables or a secret manager instead of TOOLS.md.

Risk: Token generation and API calls may expose sensitive credentials or bearer tokens in logged environments.

Mitigation: Avoid running token commands where shell history, terminal logs, or CI logs capture command output.

Risk: Automated record creation and message sending can affect workspace data or notify unintended recipients if scopes or inputs are too broad.

Mitigation: Limit Feishu app scopes to the needed record-creation and message-sending permissions and review target identifiers before bulk actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijie298/skills/feishu-enhanced)
- [Publisher profile](https://clawhub.ai/user/lijie298)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu Bitable batch create records API](https://open.feishu.cn/open-apis/bitable/v1/apps/$app_token/tables/$table_id/records/batch_create)
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$receive_id_type)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and Feishu app credentials with only the scopes needed for the intended automation.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
