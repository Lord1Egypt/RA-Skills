## Description:

Email Triage Pro helps an agent categorize, prioritize, summarize, and draft reviewable replies for emails accessed through webmail or pasted email content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to let an agent inspect a selected mailbox or pasted email content, categorize messages by urgency, summarize the inbox, and prepare reply drafts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive mailbox content through existing browser or web sessions.

Mitigation: Use it only when the user deliberately wants the agent to inspect a specific mailbox or pasted email content.

Risk: Broad casual triggers such as checking email may start inbox inspection without an explicit confirmation step.

Mitigation: Confirm the mailbox, account, and scope before fetching or reading email content.

Risk: Generated reply drafts may be incorrect, incomplete, or reveal information the user did not intend to send.

Mitigation: Require user review and editing before any draft is sent outside the agent session.

## Reference(s):

- [Email Triage Pro on ClawHub](https://clawhub.ai/tommot2/skills/email-triage-pro)
- [TommoT2 ClawHub Profile](https://clawhub.ai/user/tommot2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, category labels, and reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are presented for user review and are not sent automatically.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
