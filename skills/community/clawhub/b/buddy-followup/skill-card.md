## Description: <br>
Buddy Followup helps agents schedule one-time follow-up reminders through configured OpenClaw messaging channels after starting long-running tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiyishr](https://clawhub.ai/user/baiyishr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set reminders when a sub-agent, build, deployment, script, API call, or similar task may finish later. The follow-up prompt helps the agent check status, report results, or schedule another reminder if the task is still pending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text may be delivered to every configured OpenClaw messaging channel. <br>
Mitigation: Check configured Telegram and WhatsApp recipients before scheduling and include only short, non-sensitive task context. <br>
Risk: Follow-up messages can expose secrets, internal identifiers, private customer details, or other sensitive information if included in the reminder text. <br>
Mitigation: Keep reminder text brief and avoid sensitive or channel-inappropriate details. <br>


## Reference(s): <br>
- [Buddy Followup on ClawHub](https://clawhub.ai/baiyishr/buddy-followup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and shell output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Schedules one cron reminder per configured OpenClaw messaging channel and exits after scheduling.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
