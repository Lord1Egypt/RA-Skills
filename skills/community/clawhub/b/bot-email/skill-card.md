## Description: <br>
Get an email address without your human. Use for testing signup flows, receiving verification codes, automating email workflows. Free. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claw-silhouette](https://clawhub.ai/user/claw-silhouette) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create bot email inboxes, read received messages, extract verification codes, and monitor email-based workflows for testing or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose verification codes and authentication emails. <br>
Mitigation: Use it for bot or test-account workflows, and avoid real-user or high-value production 2FA flows unless the user explicitly accepts that risk. <br>
Risk: Generated API keys provide access to inbox contents. <br>
Mitigation: Protect API keys like passwords and store them only when the user explicitly approves a secure location. <br>
Risk: Inbox deletion endpoints can remove messages. <br>
Mitigation: Confirm destructive delete or clear-inbox actions before running them. <br>
Risk: Heartbeat monitoring can repeatedly fetch and surface email metadata. <br>
Mitigation: Enable monitoring only after the user confirms the target address and understands that sender, subject, and preview details may be shown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/claw-silhouette/bot-email) <br>
- [BotEmail.ai Documentation](https://botemail.ai/docs) <br>
- [BotEmail.ai Dashboard](https://botemail.ai/dashboard) <br>
- [BotEmail.ai Website](https://botemail.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline JSON, shell, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint guidance, bearer-token usage, inbox monitoring steps, and credential handling reminders.] <br>

## Skill Version(s): <br>
v1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
