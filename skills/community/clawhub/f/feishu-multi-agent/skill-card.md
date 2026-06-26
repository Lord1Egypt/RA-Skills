## Description: <br>
Production blueprint for orchestrating multiple OpenClaw agents via Feishu with file-driven task queues, cron scheduling, and workspace sandbox workarounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evan966890](https://clawhub.ai/user/evan966890) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up and maintain a Feishu-connected OpenClaw multi-agent workflow with a lead agent, task queues, recurring cron jobs, and operational troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Feishu-connected agents may act across workspaces, run recurring jobs, modify repositories, or send messages without enough safety controls. <br>
Mitigation: Use dedicated non-sensitive workspaces and repositories, least-privilege Feishu bots, strict task-queue paths, and manual review before git push or public messaging. <br>
Risk: Recurring cron jobs can keep agents running after the initial setup and may trigger unintended actions. <br>
Mitigation: Review every cron job before enabling it, disable jobs that are not needed, and periodically audit active sessions and task queues. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [ClawHub skill page](https://clawhub.ai/evan966890/feishu-multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with JSON examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, operational checklists, cron recipes, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
