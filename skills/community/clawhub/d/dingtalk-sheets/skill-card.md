## Description:

Helps agents create and manage DingTalk online spreadsheets, including worksheets, ranges, cell updates, searches, and CSV or TSV import and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmwei666](https://clawhub.ai/user/zmwei666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate DingTalk online spreadsheets through a configured MCP endpoint, including creating files, listing sheets, reading ranges, writing cells, finding cells, and moving data through CSV or TSV files. It is intended for spreadsheet workflows, not DingTalk document bodies, messaging, calendars, or approval flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify remote DingTalk spreadsheets.

Mitigation: Review the target spreadsheet, worksheet, range, and values before write, import, or append-style operations.

Risk: The configured DingTalk MCP URL can contain access credentials.

Mitigation: Store the endpoint in mcporter configuration or DINGTALK_MCP_SHEETS_URL and avoid exposing the actual URL in prompts, logs, or shared outputs.

Risk: Exported CSV or TSV files may contain untrusted data when other people can edit the source spreadsheet.

Mitigation: Treat exported files as untrusted and review them before opening, sharing, or importing into downstream systems.

Risk: The native append_rows tool is documented as temporarily unstable.

Mitigation: Use get_sheet to find the last non-empty row and update_range to write the next calculated range.

## Reference(s):

- [DingTalk Sheets API Reference](references/api-reference.md)
- [DingTalk Sheets Error Codes](references/error-codes.md)
- [DingTalk MCP](https://mcp.dingtalk.com)
- [ClawHub Skill Page](https://clawhub.ai/zmwei666/skills/dingtalk-sheets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with JSON arguments, shell command examples, and optional CSV or TSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the DINGTALK_MCP_SHEETS_URL credential endpoint and the mcporter binary; write and export operations depend on target spreadsheet permissions.]

## Skill Version(s):

0.0.6 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
