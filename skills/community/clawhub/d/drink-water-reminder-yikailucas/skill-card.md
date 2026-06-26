## Description: <br>
Create, manage, and remove periodic hydration reminders via OpenClaw cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YIKAILucas](https://clawhub.ai/user/YIKAILucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and agents use this skill to set, inspect, and remove recurring hydration reminders in OpenClaw. It is suited for personal productivity workflows that need periodic announcements to the current session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent recurring cron reminder until it is removed. <br>
Mitigation: Use the remove workflow when reminders are no longer needed and review existing reminders before adding a new interval. <br>
Risk: Very short intervals can produce frequent announcements. <br>
Mitigation: Choose an interval that matches the user's tolerance for reminders and avoid very short intervals unless frequent prompts are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YIKAILucas/drink-water-reminder-yikailucas) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell command examples and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates, lists, or removes an OpenClaw cron reminder named drink-water-reminder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
