## Description: <br>
Provides command templates, examples, and helper scripts for creating and validating OpenClaw scheduled cron tasks that send one-time or recurring announcements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonfc888](https://clawhub.ai/user/jasonfc888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to turn reminder or recurring automation requests into cron add/list commands, validate schedule parameters, and check that announcements are targeted to the intended channel and recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent cron jobs that send announcements. <br>
Mitigation: Explicitly verify the schedule, message, channel, and recipient before execution, and periodically list and delete cron tasks that are no longer needed. <br>
Risk: Recipient-targeting behavior is not safely implemented or clearly controlled. <br>
Mitigation: Confirm that the runtime actually supports safe channel and user extraction, or provide explicit channel and recipient values before creating a task. <br>
Risk: Task names, messages, or validation output may expose sensitive information when memory or logging is enabled. <br>
Mitigation: Avoid sensitive task names and message content, and review logs or memory records according to the deployment's data-handling policy. <br>


## Reference(s): <br>
- [Cron examples reference](references/cron-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/jasonfc888/corn-manager-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and optional shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron schedule, message, channel, recipient, and validation checks; commands may create persistent OpenClaw cron tasks when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
