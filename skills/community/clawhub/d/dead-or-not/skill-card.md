## Description: <br>
Dead Or Not periodically checks user responsiveness and, after a configured timeout and missed follow-up, sends an email alert to an emergency contact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trae1ounG](https://clawhub.ai/user/Trae1ounG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure an agent-based check-in workflow that asks whether the user is okay and emails a designated contact if the user remains unresponsive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ongoing inactivity monitoring may create unwanted surveillance or alerts if installed without clear consent and expectations. <br>
Mitigation: Install only when the user intentionally wants monitoring, document the check-in cadence, and keep clear instructions for disabling the cron job. <br>
Risk: Emergency-contact email can notify the wrong recipient or send inappropriate content if configuration is incorrect. <br>
Mitigation: Verify the recipient address and message before use, then test the full check-in and alert path before relying on it. <br>
Risk: SMTP credentials are handled through local configuration and could be exposed if the config file is too broadly readable. <br>
Mitigation: Use a dedicated email account or app-specific SMTP password and restrict permissions on the configuration file. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Trae1ounG/dead-or-not) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and script-based workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for local cron-based monitoring and SMTP email notification.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
