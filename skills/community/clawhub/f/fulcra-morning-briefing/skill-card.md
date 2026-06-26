## Description: <br>
Compose a personalized morning briefing using the latest fulcra-context skill for sleep, biometrics, calendar, activity, and weather context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect Fulcra sleep, biometric, calendar, activity, and weather context, then compose a morning briefing calibrated to the user's sleep quality. It is intended for private personal briefings rather than public or group disclosure of sensitive health and schedule details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes highly personal sleep, biometric, calendar, activity, and location-related context. <br>
Mitigation: Use it only in trusted private contexts, confirm the data categories before use, and avoid sharing exact health, calendar, or location details in group or public channels. <br>
Risk: Weather lookup behavior may send a location-derived query to wttr.in. <br>
Mitigation: Prefer coarse locations and disable or avoid external weather lookup when the user does not want location information shared with that service. <br>


## Reference(s): <br>
- [Fulcra Platform](https://fulcradynamics.com) <br>
- [Context iOS App](https://apps.apple.com/app/id1633037434) <br>
- [Fulcra Developer Docs](https://fulcradynamics.github.io/developer-docs/) <br>
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python) <br>
- [Fulcra Context MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/arc-claw-bot/fulcra-morning-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON collector output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefing detail and tone are adjusted according to sleep quality and available personal context.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
