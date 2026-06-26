## Description: <br>
Sends text messages through configurable Feishu apps using App ID and Secret authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to send plain-text Feishu messages to a configured user or group. It is useful when an agent needs a simple notification path through a Feishu app that has been approved for the intended content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text and recipient IDs are sent to Feishu. <br>
Mitigation: Use only an approved Feishu tenant and app, and avoid sending secrets, personal data, or regulated business content unless that environment is approved for it. <br>
Risk: The Feishu app secret enables authentication for message sending if exposed. <br>
Mitigation: Protect and rotate APP_SECRET, and use a least-privilege Feishu app for this skill. <br>
Risk: Agents with this skill can send messages to the configured or requested recipient. <br>
Mitigation: Install it only for agents that should be allowed to send Feishu messages, and set a narrow default recipient when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wengjianmin19850412/feishuweng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, JSON] <br>
**Output Format:** [JSON response from the Feishu API after sending a text message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu APP_ID and APP_SECRET configuration; receive_id may be supplied per call or defaulted from DEFAULT_RECEIVE_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
