## Description: <br>
Feishu online spreadsheet (Sheets) operations including create, read, write, append data, and manage worksheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wesley138cn](https://clawhub.ai/user/wesley138cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to create, inspect, update, and manage Feishu Sheets from an agent workflow using Feishu app credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials grant access to spreadsheet operations. <br>
Mitigation: Use a dedicated Feishu app with the minimum read and write scopes needed, and protect FEISHU_APP_ID and FEISHU_APP_SECRET. <br>
Risk: Write, delete, insert, and worksheet-management actions can change or remove spreadsheet content. <br>
Mitigation: Manually confirm the spreadsheet token, sheet ID, range, and action before running write or delete operations. <br>


## Reference(s): <br>
- [Feishu Sheets Skill on ClawHub](https://clawhub.ai/wesley138cn/feishu-sheets-skill) <br>
- [Feishu Sheets API Reference](references/api-reference.md) <br>
- [Feishu Sheets API Base URL](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Configuration] <br>
**Output Format:** [JSON responses from Feishu API operations, with configuration guidance for enabling the sheets tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, update, append, insert, or delete Feishu spreadsheet content depending on the selected action and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
