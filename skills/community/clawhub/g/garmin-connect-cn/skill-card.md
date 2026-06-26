## Description: <br>
Queries Garmin Connect China health data, including daily steps, distance, calories, sleep, heart rate, and recent activities, using a user-provided JWT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcyxk](https://clawhub.ai/user/tcyxk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Garmin Connect users can use this skill to answer natural-language or command-line questions about synced Garmin health data such as steps, sleep, heart rate, calories, distance, and recent activities for the China Garmin Connect service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Garmin JWT_WEB token that grants account access and can be exposed through command-line arguments, chat, shell history, or logs. <br>
Mitigation: Treat JWT_WEB like a password, prefer environment variables or local secret storage, avoid pasting it into chat or logs, and rotate it when it expires or may have been exposed. <br>
Risk: A hard-coded Garmin user ID can cause the activity query to request data for the wrong account. <br>
Mitigation: Remove the default user ID or replace it with the authenticated user's ID resolved from the user-settings endpoint before using activity queries. <br>
Risk: Returned Garmin data can include sensitive health and account information. <br>
Mitigation: Review outputs before sharing, limit retention of exported results, and use the skill only with accounts and data the user is authorized to access. <br>


## Reference(s): <br>
- [Garmin Connect API documentation](artifact/references/api.md) <br>
- [Garmin Connect setup guide](artifact/references/setup.md) <br>
- [ClawHub release page](https://clawhub.ai/tcyxk/garmin-connect-cn) <br>
- [Garmin Connect China](https://connect.garmin.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include personal health metrics returned from Garmin Connect; users should avoid sharing tokens or sensitive results in logs or chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
