## Description: <br>
Sends Markdown-formatted DingTalk group chat notifications through a configured bot webhook, with message types, mentions, and optional signed requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewqumm](https://clawhub.ai/user/andrewqumm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to push operational notifications, job status, alerts, and workflow updates into DingTalk group chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs and signing secrets are credentials that can let another party post into the configured DingTalk group. <br>
Mitigation: Store the webhook and secret in environment variables or a protected config file, rotate them if exposed, and avoid including them in prompts or shared logs. <br>
Risk: Notifications may disclose sensitive data to everyone in the target DingTalk group. <br>
Mitigation: Send only non-sensitive operational content and review automated notification templates before enabling the skill in workflows. <br>
Risk: Automated or @all messages can notify a broad audience unexpectedly. <br>
Mitigation: Restrict @all usage to intentional alerting workflows and add human review or policy checks for high-volume automation. <br>
Risk: Posting to an untrusted or non-HTTPS webhook could expose message content or credentials. <br>
Mitigation: Use the official HTTPS DingTalk robot webhook and verify webhook configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/andrewqumm/dingtalk-push) <br>
- [Publisher profile](https://clawhub.ai/user/andrewqumm) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Markdown, JSON] <br>
**Output Format:** [DingTalk Markdown webhook messages with JSON success or error results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports info, success, warning, and error message types, targeted mobile mentions, and @all notifications.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
