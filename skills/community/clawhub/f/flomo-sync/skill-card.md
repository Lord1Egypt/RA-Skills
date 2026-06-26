## Description: <br>
Syncs flomo memos to local Markdown files with incremental updates and optional attachment downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giraffe-tree](https://clawhub.ai/user/giraffe-tree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and flomo users use this skill to export flomo memos into local Markdown files for backup, migration, or personal knowledge management. It supports incremental syncs, per-memo Markdown output, and optional local attachment downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive flomo notes and an access token during sync. <br>
Mitigation: Run it only when intentionally exporting notes locally, keep .flomo.config out of chat and version control, and treat the token like a password. <br>
Risk: Attachment downloads can copy private media files to local disk. <br>
Mitigation: Use an explicit private absolute output directory and pass --no-download when local attachment copies are not desired. <br>


## Reference(s): <br>
- [flomo web app](https://v.flomoapp.com) <br>
- [flomo API base URL used by the skill](https://flomoapp.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown files with YAML front matter, local attachment paths or remote URLs, and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a flomo access token and an absolute output directory; may write .flomo.lock and downloaded attachment files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
