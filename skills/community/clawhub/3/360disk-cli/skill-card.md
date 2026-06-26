## Description: <br>
360disk-cli helps agents operate 360 AI Cloud Disk from the command line, including browsing, searching, uploading, downloading, moving, deleting, sharing, saving content, reading and writing configs, and returning structured JSON for jq pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsoncm](https://clawhub.ai/user/jsoncm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation-focused agents use this skill to manage 360 AI Cloud Disk files from scripts, CI workflows, and command-line sessions. It is suited for file management, cloud backup and restore, structured JSON output, and command composition with tools such as jq. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad cloud-file control, including deletes, overwrites, shares, restores, backups, and syncs. <br>
Mitigation: Require the agent to show exact local and cloud paths before destructive, sharing, restore, backup, or sync operations. <br>
Risk: The skill requires sensitive credentials for cloud-drive access. <br>
Mitigation: Use a least-privilege API key and avoid placing real keys in command histories, prompts, or shared logs. <br>
Risk: Auto-backup can persistently move local content to cloud storage. <br>
Mitigation: Enable auto-backup only for a narrow non-sensitive directory, verify status after enabling it, and keep the disable command available. <br>


## Reference(s): <br>
- [360disk CLI Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jsoncm/360disk-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI defaults to structured JSON and supports quiet output for downstream parsing.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
