## Description: <br>
Automatically logs into email accounts such as Gmail, Outlook, and QQ Mail to fetch messages and generate daily summaries, important-message checks, and digest reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate mailbox access with browser-use, collect recent email information, generate daily digest reports, and configure scheduled summary runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad access to logged-in mailboxes and can run recurring background mailbox access. <br>
Mitigation: Install only if broad mailbox automation is acceptable, and enable cron or launchd only when recurring access is intentional. <br>
Risk: AI extraction may send email content outside the mailbox context depending on the configured provider. <br>
Mitigation: Avoid AI extraction unless the data destination and retention behavior are understood. <br>
Risk: Screenshots and logs may contain sensitive email information. <br>
Mitigation: Delete screenshots and logs that are not needed and avoid storing sensitive mailbox content in retained files. <br>
Risk: Password entry through automation examples can expose credentials in command history or logs. <br>
Mitigation: Prefer reusing an already logged-in browser session and avoid entering passwords through scripted examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/email-daily-summary-zc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, JavaScript, XML, and report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate mailbox summary text, screenshots, logs, browser automation commands, and cron or launchd configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
