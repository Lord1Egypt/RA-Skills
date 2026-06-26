## Description: <br>
Installs and configures a Claude Code status line that shows token usage, context window percentage, git branch, and color-coded warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, inspect, and remove a local Claude Code status line for token usage, context percentage, git branch, and threshold-based color warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer changes Claude Code status line configuration and may replace an existing custom statusLine setting. <br>
Mitigation: Review the current ~/.claude/settings.json statusLine value before installing and keep a backup if the existing command should be restored later. <br>
Risk: Claude Code will run the installed local status line command after configuration. <br>
Mitigation: Install only when the user intentionally wants this local command to run, and uninstall the skill's configuration when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ajitsingh25/claude-code-statusline) <br>
- [Publisher profile](https://clawhub.ai/user/ajitsingh25) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and local JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs local Python files and updates Claude Code status line configuration under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
