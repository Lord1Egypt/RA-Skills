## Description: <br>
Export GitHub starred repositories by category and sync them to a Notion database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nick-tsyen](https://clawhub.ai/user/nick-tsyen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub users use this skill to export starred repositories into categorized Markdown and synchronize that collection into a structured Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion sync script sends a Notion token over requests with TLS certificate verification disabled. <br>
Mitigation: Review and patch the sync script before use; avoid running the sync until TLS verification is enabled. <br>
Risk: The Notion sync can archive or overwrite existing database entries during refresh. <br>
Mitigation: Use a dedicated or backed-up Notion database, pass an explicit --parent-id, and confirm the target before syncing. <br>
Risk: The sync relies on Notion workspace credentials and writes persistent local sync state. <br>
Mitigation: Use a least-privilege Notion integration and keep generated state and exported data out of shared commits unless intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nick-tsyen/dataninja-github-stars-export) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nick-tsyen) <br>
- [Export GitHub Stars Script](references/export_stars.md) <br>
- [Sync Stars to Notion DB](references/sync_stars.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>
- [Notion Developers](https://developers.notion.com/) <br>
- [jq](https://jqlang.github.io/jq/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python command examples; generated artifacts include a Markdown export and Notion database rows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated GitHub CLI, jq, requests, and NOTION_API_KEY; sync state is tracked in assets/.notion_sync_config.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
