## Description: <br>
Feishu Cli helps an agent use the Feishu command line tool to convert Markdown and Feishu documents and manage docs, wikis, spreadsheets, messages, calendars, tasks, permissions, and cloud space resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niesongyang](https://clawhub.ai/user/niesongyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an agent to perform Feishu workspace operations through feishu-cli, including document conversion, content import or export, messaging, scheduling, task creation, and collaborator permission changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to write Feishu documents or spreadsheets, send messages, create events or tasks, import or export sensitive content, and change collaborator permissions. <br>
Mitigation: Use a dedicated least-privileged Feishu app and require explicit manual confirmation before any write, messaging, export, scheduling, task, or permission-changing command is run. <br>
Risk: The installation path references a remote GitHub installer. <br>
Mitigation: Inspect and pin the installer or release artifact before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niesongyang/feishu-cli) <br>
- [Publisher profile](https://clawhub.ai/user/niesongyang) <br>
- [Feishu CLI releases](https://github.com/riba2534/feishu-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and feishu-cli command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in Feishu API side effects when an agent follows the command guidance with valid credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
