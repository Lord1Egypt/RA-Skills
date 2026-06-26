## Description: <br>
Feishu Sheets (Fixed) helps agents create, read, write, append, and manage Feishu online spreadsheets and worksheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knight-ni](https://clawhub.ai/user/knight-ni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to work with Feishu Sheets, including creating spreadsheets, reading and writing cell ranges, appending rows, and managing worksheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials can grant access to spreadsheet content. <br>
Mitigation: Use a dedicated Feishu app with the narrowest scopes needed and prefer read-only credentials when editing is not required. <br>
Risk: Write, append, row or column deletion, and worksheet deletion actions can change or remove spreadsheet data. <br>
Mitigation: Confirm spreadsheet tokens, sheet IDs, ranges, and delete actions before allowing writes or deletions. <br>


## Reference(s): <br>
- [Feishu Sheets API Reference](references/api-reference.md) <br>
- [ClawHub skill release](https://clawhub.ai/knight-ni/feishu-sheets-fixed) <br>
- [Feishu Open Platform API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON action examples and Feishu API response JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and spreadsheet identifiers for live API operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
