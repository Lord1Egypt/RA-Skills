## Description: <br>
Helps an agent send DingTalk messages through webhook bots, enterprise app robots, work notifications, and session webhooks, including Markdown or card messages, recalls, and read-status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breath57](https://clawhub.ai/user/breath57) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workplace operators use this skill to prepare and send DingTalk notifications or chat messages from an agent after confirming the channel, recipients, credentials, and message content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send workplace messages using saved DingTalk credentials. <br>
Mitigation: Use a dedicated low-privilege DingTalk bot or app and confirm recipient, channel, and content before sending. <br>
Risk: Saved credentials in ~/.dingtalk-skills/config may be reused across sessions. <br>
Mitigation: Protect the config file and remove stored credentials when they should no longer be reused. <br>


## Reference(s): <br>
- [DingTalk Message API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON request bodies, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare API calls that send DingTalk messages using user-provided or saved credentials.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
