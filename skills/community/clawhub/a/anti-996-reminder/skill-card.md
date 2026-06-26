## Description: <br>
Sends scheduled noon and bedtime wellness reminders, supports sleep check-ins with points and streaks, and can post a weekly sleep check-in summary for WeChat or QQ channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devioslang](https://clawhub.ai/user/devioslang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and bot operators use this skill to schedule gentle rest reminders, encourage earlier sleep, track sleep check-ins, and send a short weekly progress summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled reminders may be delivered to the wrong chat if sample account or recipient IDs are reused. <br>
Mitigation: Review and replace the account and recipient IDs before enabling schedules, and enable them only for intended chats. <br>
Risk: The points file stores personal habit data about sleep check-ins. <br>
Mitigation: Treat points.json as personal habit data and prefer direct-message or explicit-command use when the bot is present in group conversations. <br>


## Reference(s): <br>
- [Anti 996 Reminder on ClawHub](https://clawhub.ai/devioslang/anti-996-reminder) <br>
- [devioslang publisher profile](https://clawhub.ai/user/devioslang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and scheduled chat message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces randomized reminder text from JSON content pools and updates local check-in point state.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
