## Description: <br>
Guides an AI agent through installing and authenticating the agentdrive CLI, backing up its own root/data directory to 360AgentDrive, enabling auto-backup, and maintaining a recurring backup guard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsoncm](https://clawhub.ai/user/jsoncm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent operators and developers use this skill when they want an agent to configure 360AgentDrive authentication, install or update the agentdrive CLI, back up the agent's own root/data directory, and enable recurring backup monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to upload its full root/data directory to 360AgentDrive, which may include credentials or private data. <br>
Mitigation: Require visible confirmation of the exact source path and cloud destination before backup, and add explicit exclusions for credentials and private data. <br>
Risk: The skill can enable recurring auto-backup behavior and a scheduled guard with limited user control. <br>
Mitigation: Make the recurring guard optional, document the removal command, and confirm that the user wants ongoing background backup before enabling it. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/jsoncm/agentdrive-backup) <br>
- [360AgentDrive homepage](https://agentdrive.360.cn) <br>
- [360AgentDrive CLI documentation](https://agentdrive.360.cn/cli) <br>
- [360AgentDrive CLI installation](https://agentdrive.360.cn/cli/installation) <br>
- [360AgentDrive CLI commands](https://agentdrive.360.cn/cli/commands) <br>
- [360AgentDrive CLI advanced usage](https://agentdrive.360.cn/cli/advanced) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational steps for OAuth/API-key login, CLI installation, root-directory selection, initial backup, auto-backup enablement, and scheduled guard setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
