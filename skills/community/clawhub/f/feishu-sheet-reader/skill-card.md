## Description: <br>
Read data from Feishu Sheets via the Feishu API, including specific ranges, entire sheets, and sheet metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-xun](https://clawhub.ai/user/jack-xun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to fetch rows or metadata from Feishu spreadsheet links for review, analysis, or reformatting inside an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Feishu app credentials to access spreadsheet data. <br>
Mitigation: Install it only with trusted Feishu credentials and grant the app the least privileges needed for the sheets being read. <br>
Risk: A missing or broad range can cause the skill to read more sheet data than intended. <br>
Mitigation: Confirm the spreadsheet link, sheet ID, and range before execution, and avoid full-sheet reads when sensitive data may be present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-xun/feishu-sheet-reader) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu sheet values API](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values/{range}) <br>
- [Feishu sheet metadata API](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Tab-separated text plus Markdown guidance with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Feishu app credentials; when no sheet ID or range is supplied, it may select the first sheet and read the whole sheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
