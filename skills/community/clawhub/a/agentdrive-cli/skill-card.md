## Description: <br>
AgentDrive CLI lets agents manage 360 AI Cloud Drive files through shell commands for browsing, search, upload and download, move and rename, delete, sharing, saving content, appending files, configuration reads and writes, user info, and JSON pipeline workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsoncm](https://clawhub.ai/user/jsoncm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation users, and agents use this skill to turn cloud-drive file-management requests into AgentDrive CLI commands for interactive work, scripts, and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run destructive cloud-drive operations such as delete, clear-dir, overwrite or replace, restore, logout, backup, and auto-backup changes. <br>
Mitigation: Require explicit user confirmation and target-path review before running destructive or persistent commands. <br>
Risk: The skill handles AgentDrive credentials and can persist authentication data in local configuration. <br>
Mitigation: Prefer an environment variable or protected config, and avoid placing API keys directly in command text or logs. <br>
Risk: Using the latest npm package can change CLI behavior between runs. <br>
Mitigation: Pin @aicloud360/agentdrive to an exact version for CI, audits, and repeatable workflows. <br>
Risk: Backup, restore, and auto-backup commands can affect local folders and cloud content beyond a single command. <br>
Mitigation: Scope source and destination folders narrowly and confirm before enabling auto-backup or restoring cloud content locally. <br>


## Reference(s): <br>
- [AgentDrive CLI command reference](references/commands.md) <br>
- [AgentDrive CLI skill README](README.md) <br>
- [ClawHub release page](https://clawhub.ai/jsoncm/agentdrive-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands usually return structured JSON and may be piped to jq; sensitive API keys should be passed through environment variables or protected configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
