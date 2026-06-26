## Description: <br>
Set up a daily countdown reminder for a stock's next price-moving corporate event, including earnings releases, AGMs, product launches, investor days, dividend dates, FDA decisions, or other events likely to affect the stock price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investors use this skill to set up daily reminders before a public company's next significant corporate event. The skill helps resolve the company ticker, discover or confirm the event, and schedule recurring countdown briefings with price and fundamentals checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create automated daily stock-event messages in the selected chat. <br>
Mitigation: Confirm the event date, reminder start timing, timezone, and delivery chat before approving the cron reminder. <br>
Risk: Countdown briefings depend on externally sourced event and market data that may be delayed, missing, or incorrect. <br>
Mitigation: Review the discovered event source and cancel or update the reminder when the tracked event changes or the briefings are no longer needed. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [ClawHub skill release](https://clawhub.ai/youpele52/event-countdown-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and reminder configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a daily cron reminder that runs stock price and fundamentals checks until the confirmed event date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
