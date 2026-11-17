## Description:

Read data from Feishu Sheets by parsing shared sheet links, fetching specific ranges or entire sheets, and listing sheet metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-xun](https://clawhub.ai/user/jack-xun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read Feishu spreadsheet data supplied by a user, inspect a selected sheet or range, and return tab-separated data for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use configured Feishu app credentials to read spreadsheet contents.

Mitigation: Use least-privileged Feishu app credentials and confirm that each requested sheet is approved for access before running the reader.

Risk: Feishu app secrets and bearer tokens may be exposed through curl command arguments during HTTP requests.

Mitigation: Prefer safer HTTP handling that avoids putting secrets in process arguments, and avoid running the script on shared systems where process details may be visible.

Risk: Reading an entire sheet or the first detected sheet may retrieve more data than the user intended.

Mitigation: Request an explicit sheet ID and range when possible, and review the target URL, sheet, and range before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jack-xun/skills/feishu-sheet-reader)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu sheet values API](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values/{range})
- [Feishu sheet metadata API](https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/sheets/query)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and tab-separated sheet data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and network access to the Feishu Open API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
