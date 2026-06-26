## Description: <br>
Feishu Sheets Toolkit helps an agent create, read, write, append, and manage Feishu online spreadsheets and worksheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent prepare Feishu Sheets API requests and operations for spreadsheet creation, data reads and writes, row or column edits, and worksheet management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu credentials can grant access to spreadsheet and drive data. <br>
Mitigation: Use a dedicated Feishu app with the narrowest required Sheets and Drive permissions, and avoid admin or tenant-wide credentials. <br>
Risk: The skill can delete worksheets, delete rows or columns, or overwrite spreadsheet ranges. <br>
Mitigation: Require explicit human confirmation before destructive actions or large range writes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiuwenxi416488212-ship-it/feishu-sheets-toolkit) <br>
- [Feishu Sheets API Reference](references/api-reference.md) <br>
- [Feishu Sheets API v2](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets) <br>
- [Feishu Sheets API v3](https://open.feishu.cn/open-apis/sheets/v3/spreadsheets) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, YAML, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and tenant access tokens for live API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
