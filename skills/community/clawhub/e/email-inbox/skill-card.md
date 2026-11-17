## Description:

Email Inbox Triage summarizes, prioritizes, and groups incoming email, extracts actions and deadlines, and drafts replies when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangweifen2025-dotcom](https://clawhub.ai/user/fangweifen2025-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and assistants use this skill to review mailbox contents, find important unread or recent messages, identify deadlines and requested actions, and prepare concise reply drafts when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email messages can contain sensitive personal, business, financial, or legal information.

Mitigation: Review mailbox connector permissions before use and limit the agent to the mailbox content needed for the current task.

Risk: Reply drafts or priority judgments can be incorrect or incomplete.

Mitigation: Verify drafted replies, extracted deadlines, and recommended next steps before sending messages or taking action.

Risk: A user may expect the skill to send mail automatically.

Mitigation: The skill should only prepare drafts or send email after an explicit user request and review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangweifen2025-dotcom/skills/email-inbox)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, priority lists, next steps, and reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include grouped message summaries, extracted deadlines, requested actions, and placeholders for missing reply details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
