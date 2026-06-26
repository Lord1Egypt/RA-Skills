## Description: <br>
Manage and create scheduled cron jobs, automated monitoring tasks, reminders, and periodic push notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mr-chen-05](https://clawhub.ai/user/Mr-chen-05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to create, inspect, update, and troubleshoot recurring cron-based automations for monitoring, reminders, reports, and notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, modify, or delete recurring scheduled automations. <br>
Mitigation: Require explicit user confirmation before changing or deleting cron jobs, and restrict the jobs the skill is allowed to control. <br>
Risk: Automation outputs may be stored long-term in local intelligence logs. <br>
Mitigation: Review the contents of intel/daily logs and define a retention or deletion practice before relying on the skill for ongoing monitoring. <br>
Risk: Reports may be sent to external delivery services. <br>
Mitigation: Enable only trusted delivery channels and use least-privilege credentials for each configured service. <br>


## Reference(s): <br>
- [Cron Automation Manager README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Delivery Configuration Example](artifact/config/delivery-config.example.json) <br>
- [Task Creator Module](artifact/modules/task-creator.md) <br>
- [Delivery Router Module](artifact/modules/delivery-router.md) <br>
- [Health Check Module](artifact/modules/health-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cron configuration snippets and delivery configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update scheduled automation definitions, local intelligence logs, and delivery settings when the agent applies the guidance.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
