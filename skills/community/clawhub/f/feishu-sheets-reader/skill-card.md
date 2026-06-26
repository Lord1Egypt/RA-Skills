## Description: <br>
Provides Feishu Sheets operations for creating, reading, writing, appending, and managing online spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lens-lzy](https://clawhub.ai/user/Lens-lzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Feishu Sheets: create spreadsheets, read and write ranges, append rows, manage worksheets, and insert or delete rows or columns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials can modify or delete spreadsheet data, including ranges, rows, columns, and worksheets. <br>
Mitigation: Use a least-privilege Feishu app, test outside production, and require confirmation of the exact spreadsheet token, sheet ID, range, and action before write or delete operations. <br>
Risk: Broad Drive or spreadsheet permissions may expose more cloud data than intended. <br>
Mitigation: Restrict the app to required scopes and approved spreadsheets, and avoid broad Drive access until the integration has been reviewed. <br>


## Reference(s): <br>
- [Feishu Sheets API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/Lens-lzy/feishu-sheets-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and explicit spreadsheet token, sheet ID, and range inputs for operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
