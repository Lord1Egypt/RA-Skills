## Description: <br>
Helps an agent manage DingTalk online spreadsheets, including creating sheets, reading ranges, writing cells, finding cells, and importing or exporting CSV and TSV data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmwei666](https://clawhub.ai/user/zmwei666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate DingTalk Sheets through mcporter when they need to create spreadsheets, inspect worksheets, read or update ranges, search cells, or move data between DingTalk Sheets and local CSV or TSV files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The DingTalk MCP Sheets URL may include an access token. <br>
Mitigation: Treat DINGTALK_MCP_SHEETS_URL as a secret and refer to it by environment variable or placeholder rather than exposing the URL. <br>
Risk: Spreadsheet write or export actions can affect the wrong sheet, range, or local file. <br>
Mitigation: Confirm the target sheet, range, and output filename before allowing writes or exports, and keep imports and exports inside the intended workspace. <br>
Risk: The direct append_rows tool is documented as temporarily unreliable. <br>
Mitigation: Use get_sheet to identify the next empty range and update_range to append rows until append_rows is explicitly verified as stable. <br>
Risk: The import_sheet.py helper currently references an undefined APPEND_ROWS_MODE symbol. <br>
Mitigation: Review or patch import_sheet.py before relying on that helper for local CSV or TSV imports. <br>


## Reference(s): <br>
- [DingTalk Sheets Skill Page](https://clawhub.ai/zmwei666/dingtalk-sheets) <br>
- [DingTalk MCP Marketplace](https://mcp.dingtalk.com) <br>
- [API Reference](references/api-reference.md) <br>
- [Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional CSV or TSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and DINGTALK_MCP_SHEETS_URL to connect to DingTalk Sheets.] <br>

## Skill Version(s): <br>
0.0.6 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
