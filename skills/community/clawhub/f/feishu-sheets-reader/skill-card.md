## Description:

Enables an agent to create, read, write, append, and manage Feishu Sheets spreadsheets and worksheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lens-lzy](https://clawhub.ai/user/lens-lzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent operate Feishu online spreadsheets, including reading ranges, writing values, appending rows, changing sheet dimensions, and managing worksheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete Feishu spreadsheet data, including worksheet deletion and row or column deletion.

Mitigation: Use least-privilege Feishu app scopes and require human confirmation or backups before delete_sheet or delete_dimension actions.

Risk: Spreadsheet values may be exposed through shell command arguments or command output.

Mitigation: Avoid using this skill for sensitive cell values through shell commands, and limit access to credentials and terminal logs.

## Reference(s):

- [Feishu Sheets API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/lens-lzy/skills/feishu-sheets-reader)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration, Guidance]

**Output Format:** [JSON API responses with concise setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and spreadsheet permissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
