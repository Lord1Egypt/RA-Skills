## Description: <br>
Uses Volcano Engine Voice Service APIs to send voice notifications to specified phone numbers and select voice resources by language or keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent send phone-based voice notifications through a configured Volcengine account. It queries available number pools and voice resources, chooses a matching resource from the user's request, and sends the notification. <br>

### Deployment Geography for Use: <br>
Global, subject to Volcengine Voice Service availability and applicable telecom rules. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound voice notifications using the user's Volcengine account. <br>
Mitigation: Require explicit confirmation of the recipient phone number, selected voice resource or content, provider, and send action before every notification. <br>
Risk: Credentials with broad Volcengine permissions could increase impact if the agent or environment is misused. <br>
Mitigation: Use credentials with only the minimum Volcengine permissions needed for querying voice resources, querying number pools, and sending approved voice notifications. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-voice-notify) <br>
- [Volcengine signing mechanism documentation](https://www.volcengine.com/docs/6358/166389?lang=zh) <br>
- [Volcengine voice resource list documentation](https://www.volcengine.com/docs/6358/1722078?lang=zh) <br>
- [Volcengine single voice notification documentation](https://www.volcengine.com/docs/6358/172952?lang=zh) <br>
- [Volcengine number pool list documentation](https://www.volcengine.com/docs/6358/173339?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY environment variables and can trigger outbound voice notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
