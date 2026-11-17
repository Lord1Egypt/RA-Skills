## Description:

Imports local CSV, Excel, or JSON data into Feishu Bitable, with field type inference, table creation support, and incremental, full, or append sync modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanlansss](https://clawhub.ai/user/guanlansss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to import exported business data, reports, or records from local files into Feishu Bitable for team collaboration and recurring data synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full sync mode can delete all existing records in the target Feishu Bitable table.

Mitigation: Use full mode only after confirming the app_token and table_id and keeping a current backup of the target table.

Risk: Setup guidance requests an extra document-read permission that is not needed for the Bitable import flow.

Mitigation: Limit Feishu application permissions to the target Bitable resources and remove unused document-read scope before installation.

Risk: Imported local file contents are transmitted to Feishu through API calls.

Mitigation: Review source files for sensitive data and confirm the target Feishu workspace and table are appropriate before syncing.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Run the scripts in an isolated Python environment with reviewed, pinned dependency versions.

## Reference(s):

- [How to get app_token and table_id](references/get-id-guide.md)
- [Feishu Open Platform - Bitable API](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNkozM)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Python scripts that read local data files and call Feishu APIs when the user provides credentials and target Bitable identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
