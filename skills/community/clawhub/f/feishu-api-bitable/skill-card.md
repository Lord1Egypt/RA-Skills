## Description: <br>
Feishu Bitable API skill for creating, reading, updating, and deleting Feishu Bitable tables, records, fields, and views. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StevenLikeWatermelon](https://clawhub.ai/user/StevenLikeWatermelon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to manage Feishu Bitable data through a Node.js CLI and API client. It supports table, record, field, and view workflows for data synchronization, task tracking, reporting, and system integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live Feishu Bitable workspace data. <br>
Mitigation: Use a least-privilege Feishu app and require explicit confirmation before update, delete, or batch operations. <br>
Risk: FEISHU_APP_SECRET values and .env files can expose Feishu app credentials. <br>
Mitigation: Store credentials in a protected secret path or environment manager and avoid committing secret-bearing files. <br>
Risk: JSON payloads loaded from @file paths can submit unintended table or record changes. <br>
Mitigation: Review every @file JSON path and payload before running create, update, delete, or batch commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/StevenLikeWatermelon/feishu-api-bitable) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Bitable API](https://open.feishu.cn/open-apis/bitable/v1) <br>
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, JSON, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON payloads, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET; operations target caller-provided app tokens, table IDs, record IDs, and JSON payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
