## Description:

Feishu Sheets Toolkit helps agents create, read, write, append, and manage Feishu online spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Feishu Sheets actions for spreadsheet automation, including creating spreadsheets, reading and writing cell ranges, appending rows, and managing worksheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter remote Feishu Sheets, including writing values, appending rows, deleting rows or columns, deleting worksheets, changing protection, and find-and-replace operations.

Mitigation: Use test spreadsheets first, keep backups or version history, and require explicit human confirmation before destructive or broad write operations.

Risk: The server security summary reports under-described management capabilities without clear safeguards.

Mitigation: Review requested actions before execution and limit enabled Feishu permissions to the smallest set needed for the workflow.

Risk: The executable client requires Feishu app credentials and tenant access tokens to access spreadsheet data.

Mitigation: Store credentials outside prompts and shared files, rotate exposed credentials, and scope Feishu app permissions to intended spreadsheets where possible.

## Reference(s):

- [Feishu Sheets API Reference](artifact/references/api-reference.md)
- [Feishu Sheets API v2](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets)
- [Feishu Sheets API v3](https://open.feishu.cn/open-apis/sheets/v3/spreadsheets)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [ClawHub Skill Page](https://clawhub.ai/qiuwenxi416488212-ship-it/skills/feishu-sheets-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and Python or shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu Sheets action payloads and JSON API responses when the included client is executed with valid Feishu credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
