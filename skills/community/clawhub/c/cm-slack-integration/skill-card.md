## Description: <br>
Slack messaging - send messages, manage channels, upload files, add reactions, and automate team notifications via CLI and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to prepare Slack Web API commands for workspace messaging, channel workflows, file sharing, reactions, and automated notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slack OAuth or API tokens can grant access to workspace content and write actions. <br>
Mitigation: Use the least-privileged Slack token available, store it only in SLACK_TOKEN, and revoke access when the skill is no longer needed. <br>
Risk: Commands can post, update, schedule, or upload content to the wrong workspace or channel. <br>
Mitigation: Confirm the workspace, channel ID, and message payload before executing any write operation. <br>
Risk: Messages, files, or logs sent to Slack may expose sensitive information. <br>
Mitigation: Review payloads before sending and avoid posting secrets, raw logs, or confidential data. <br>


## Reference(s): <br>
- [ClawHub Slack Integration release](https://clawhub.ai/charlie-morrison/cm-slack-integration) <br>
- [Slack App configuration](https://api.slack.com/apps) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [Slack conversations.list API](https://slack.com/api/conversations.list) <br>
- [Slack files external upload API](https://slack.com/api/files.getUploadURLExternal) <br>
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Slack token supplied through SLACK_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
