## Description: <br>
Sets up a dedicated Resend-backed email address for an agent, including sending, inbound webhook receiving, inbox storage, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[di5cip1e](https://clawhub.ai/user/di5cip1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to give an agent a dedicated email identity for account verification, notifications, and controlled email handling in a Node/Express backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill configures an autonomous email inbox with full email-provider credentials and weakly scoped access controls. <br>
Mitigation: Install only when an agent-operated email address is intended; limit the Resend API key where possible and store secrets in a dedicated secrets manager. <br>
Risk: Inbox files and mail logs may expose sensitive email content if server access is broad. <br>
Mitigation: Add authentication to inbox read and acknowledgement endpoints, and restrict who can read mail/inbox and mail.log. <br>
Risk: Automated inbox monitoring can process incoming messages without enough operator control. <br>
Mitigation: Make the cron monitor explicit, reversible, and easy to disable before using it in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/di5cip1e/director-email-setup) <br>
- [Skill instructions](SKILL.md) <br>
- [Inbound email route reference](references/inboundEmail.js) <br>
- [Agent email helper reference](references/directorMail.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with JavaScript examples, JSON configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for Resend domain verification, webhook registration, secret configuration, inbox storage, monitoring, and test flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
