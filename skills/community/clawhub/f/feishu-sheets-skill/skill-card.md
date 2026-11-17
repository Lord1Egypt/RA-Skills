## Description:

Feishu online spreadsheet operations for creating spreadsheets, reading and writing cell values, appending rows, inserting or deleting rows and columns, and managing worksheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wesley138cn](https://clawhub.ai/user/wesley138cn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to automate Feishu Sheets workflows, including creating spreadsheets, reading or writing ranges, appending tabular data, and managing worksheet structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete remote Feishu spreadsheet data.

Mitigation: Verify spreadsheet tokens, sheet IDs, ranges, and delete actions before execution, and keep a backup or recovery path for important sheets.

Risk: Using the skill requires Feishu app credentials with access to spreadsheet and drive resources.

Mitigation: Install only when the agent is trusted with the required Feishu app credentials and scope credentials to the minimum needed permissions.

## Reference(s):

- [Feishu Sheets API Reference](artifact/references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/wesley138cn/skills/feishu-sheets-skill)
- [Feishu Sheets API v2 base URL](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets)
- [Feishu Sheets API v3 base URL](https://open.feishu.cn/open-apis/sheets/v3/spreadsheets)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON action examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and spreadsheet, worksheet, and range identifiers for most operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
