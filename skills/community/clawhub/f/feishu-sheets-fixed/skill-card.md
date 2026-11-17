## Description:

Feishu online spreadsheet (Sheets) operations including create, read, write, append data, and worksheet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knight-ni](https://clawhub.ai/user/knight-ni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent create, inspect, update, append to, and manage worksheets in Feishu Sheets through the Feishu Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use tenant app credentials to read, write, and delete live Feishu spreadsheet data without built-in confirmation or guardrails.

Mitigation: Install it only when spreadsheet management is intended, grant least-privileged Feishu scopes, and restrict the app to the intended spreadsheets.

Risk: Delete-row, delete-column, and delete-worksheet actions can affect production or business-critical sheets.

Mitigation: Require explicit human confirmation and preferably a backup or preview before any destructive operation.

## Reference(s):

- [Feishu Sheets API Reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/knight-ni/skills/feishu-sheets-fixed)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell command patterns, configuration snippets, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu Sheets API call instructions and JSON payload or response structures for agent tool use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
