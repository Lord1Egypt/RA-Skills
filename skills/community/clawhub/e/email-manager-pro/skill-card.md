## Description: <br>
Email Manager is an OpenClaw email attendant that checks, sorts, and summarizes connected mailboxes, highlights important messages, manages spam, drafts replies for approval, and maintains email workflow state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent manage an already-connected email account: process inbox messages, route mail into priority and workflow folders, identify spam, prepare daily reports, and draft replies that require user approval before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically reorganize an already-connected mailbox, including moving messages into spam, priority, waiting-reply, and processed folders. <br>
Mitigation: Confirm which inboxes are in scope before enabling scheduled runs, review folder and spam decisions during initial use, and keep a clear recovery path for messages moved incorrectly. <br>
Risk: The skill persists sensitive email workflow metadata such as important-message logs, sent-history cache entries, activity counters, and daily report history. <br>
Mitigation: Limit stored state to the minimum needed for routing and reporting, periodically prune retained logs, and avoid storing full message bodies unless the user explicitly needs them. <br>
Risk: Scheduled processing can repeatedly act on new mailbox content without the user present. <br>
Mitigation: Confirm check intervals and monitored inboxes during setup, make scheduled jobs easy to pause, and require user approval for new folders outside the documented standard and approved-newsletter cases. <br>
Risk: Phone or Twilio notifications may expose sender, subject, and email summaries outside the mailbox environment. <br>
Mitigation: Disable or redact phone notifications unless the user has confirmed the channel, recipients, and acceptable detail level for email alerts. <br>


## Reference(s): <br>
- [Email Manager ClawHub listing](https://clawhub.ai/encryptshawn/email-manager-pro) <br>
- [Rules and state reference](references/rules-and-state.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration, API calls] <br>
**Output Format:** [Markdown and structured email-tool actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-facing summaries, folder and schedule updates, draft email text, notification logs, and daily reports; each processing run handles up to 50 emails per inbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
