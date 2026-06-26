## Description: <br>
Sets up daily OpenClaw cron jobs for detected agents so each agent is prompted to summarize completed work into a diary file at 23:30. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RenchZhao](https://clawhub.ai/user/RenchZhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to automate daily work summaries across all configured agents. It is useful when teams want each agent to keep a dated diary without manually creating recurring prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script creates persistent daily automation for every detected OpenClaw agent. <br>
Mitigation: Review the affected agents before running it, confirm how to list and delete the created OpenClaw cron jobs, and narrow the script if only specific agents should receive daily prompts. <br>
Risk: The security summary notes unsafe shell command construction. <br>
Mitigation: Review the command construction before execution and consider replacing shell-based calls with argument-list subprocess calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RenchZhao/auto-daily-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the setup script creates OpenClaw cron configuration through CLI calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the script creates persistent daily summary jobs for detected OpenClaw agents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
