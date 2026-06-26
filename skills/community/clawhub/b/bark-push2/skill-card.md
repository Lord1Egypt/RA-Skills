## Description: <br>
Sends Bark push notifications from a Node.js skill using LobeHub-style message and title arguments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallersoup](https://clawhub.ai/user/smallersoup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send Bark notifications from agent workflows by providing a message and optional title. It requires Node.js and a Bark key, normally supplied through BARK_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches a parent USER.md file for a Bark key when BARK_KEY is not set. <br>
Mitigation: Prefer explicit BARK_KEY configuration, avoid storing the Bark key in shared or logged USER.md files, and rotate the key if it may have been exposed. <br>
Risk: Notification text and the Bark key are sent to api.day.app. <br>
Mitigation: Use the skill only for notification content and credentials that are acceptable to send to Bark. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallersoup/bark-push2) <br>
- [Bark API endpoint](https://api.day.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Console text and HTTPS request to the Bark API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Bark key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
