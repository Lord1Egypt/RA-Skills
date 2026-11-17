## Description:

Fetches recent emails from Gmail and provides concise summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbdyno](https://clawhub.ai/user/bbdyno)

### License/Terms of Use:

MIT

## Use Case:

Employees and individual Gmail users use this skill to review unread Gmail messages through concise summaries, key points, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private Gmail content and OAuth tokens.

Mitigation: Install only when read-only Gmail access is acceptable; keep credentials and token.json in a private local directory with restricted permissions.

Risk: Email content and free-form arguments can create unsafe instruction boundaries.

Mitigation: Treat email content as untrusted data, avoid passing free-form arguments, and require separate confirmation before following instructions contained in emails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bbdyno/skills/email-summary)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API read-only OAuth scope](https://www.googleapis.com/auth/gmail.readonly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summaries derived from JSON email data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Gmail OAuth credentials via GMAIL_CREDENTIALS_PATH, and read-only Gmail API access.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
