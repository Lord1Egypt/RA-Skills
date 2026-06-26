## Description: <br>
飞书增强套件 - 深度集成飞书文档、多维表格、消息和日历的自动化操作。适用于需要高效办公自动化的中文用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiJie298](https://clawhub.ai/user/LiJie298) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, operators, and developers use this skill to automate Feishu documents, Bitable records, messaging, and calendar-related office workflows for Chinese-language teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful Feishu app credentials. <br>
Mitigation: Use a least-privilege Feishu app and store FEISHU_APP_ID and FEISHU_APP_SECRET in an environment or secret-management mechanism rather than prompt-visible notes. <br>
Risk: Automated Feishu messages and bulk Bitable record creation can affect team data or notify unintended recipients. <br>
Mitigation: Review recipients, table IDs, and payloads before sending messages or creating records in bulk. <br>
Risk: The publisher is low-trust-tier third-party evidence, even though the security verdict is clean. <br>
Mitigation: Install only when the publisher is trusted and the Feishu automation capabilities are needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LiJie298/feishu-enhanced) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu Bitable batch-create records API endpoint](https://open.feishu.cn/open-apis/bitable/v1/apps/$app_token/tables/$table_id/records/batch_create) <br>
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$receive_id_type) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus authorized Feishu app credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
