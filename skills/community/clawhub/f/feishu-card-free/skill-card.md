## Description: <br>
Sends basic Feishu text cards to users or groups, with title and header color options and a safe-send workflow for shell-sensitive text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to send basic Feishu notification cards to an Open ID or group chat from agent workflows. It is suited to simple operational notices that need plain text, a title, and a supported header color. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages and optional callback data can leave the local environment. <br>
Mitigation: Review message text for secrets or personal data, verify the Feishu target ID, and use callback_url only for trusted endpoints. <br>
Risk: The skill depends on separately installed Feishu authentication and sending code that is not included in this artifact. <br>
Mitigation: Inspect and approve the feishu-common, send.js, and send_safe.js implementation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-card-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for sending simple Feishu cards; generated messages may leave the local environment through Feishu or a configured callback URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
