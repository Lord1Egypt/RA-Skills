## Description: <br>
Set up daily earnings countdown reminders for stocks by resolving a ticker, fetching the next earnings date, and scheduling recurring briefings with price and fundamentals updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to schedule daily countdown reminders ahead of company earnings releases. It creates a recurring workflow that checks the countdown, gathers price and fundamentals context, and cancels the reminder on earnings day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reminder may be configured with the wrong ticker, timezone, delivery chat, notification time, or first firing date. <br>
Mitigation: Confirm the ticker, timezone, delivery chat, daily time, cancellation behavior, and first expected reminder before creating the recurring reminder. <br>
Risk: The reminder command may not clearly pass a separate future start date. <br>
Mitigation: Verify when the first reminder will fire before confirming setup, especially when the earnings date is close. <br>
Risk: Public earnings data may be unavailable for a ticker or may not include a scheduled upcoming earnings date. <br>
Mitigation: Stop without creating a reminder when no earnings date is returned, and tell the user what could not be verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youpele52/earnings-countdown) <br>
- [Publisher profile](https://clawhub.ai/user/youpele52) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and human-readable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and openclaw; uses public earnings data to configure a daily reminder workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
