## Description:

Automate email processing: smart triage, auto-categorization, draft replies, and inbox zero. Works with Gmail, Outlook, and IMAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to triage email, categorize messages, draft replies, summarize inbox activity, and guide Gmail, Outlook, or IMAP setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials or tokens may grant sensitive email access.

Mitigation: Use least-privilege OAuth or scoped app-specific credentials, store secrets outside shared workspaces, and rotate tokens if exposed.

Risk: Automatic archiving can move or hide messages before the user has reviewed behavior.

Mitigation: Set AUTO_ARCHIVE=false until rules and categories have been reviewed against a test account or low-risk mailbox.

Risk: The documented test mode should not be treated as a no-write dry run for connected mailbox integrations.

Mitigation: Confirm provider-side permissions and run with non-production credentials before enabling actions on a real inbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/email-automation)
- [Google Cloud Console](https://console.cloud.google.com)
- [Microsoft Azure Portal](https://portal.azure.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with shell command snippets and generated email summaries, categories, and reply drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mailbox triage guidance, reply draft text, category labels, inbox summaries, and setup steps.]

## Skill Version(s):

1.2.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
