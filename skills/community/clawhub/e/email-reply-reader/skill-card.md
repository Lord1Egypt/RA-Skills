## Description:

Reads and parses job application email replies from Gmail, then classifies recruiter responses and follow-up needs for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxty](https://clawhub.ai/user/xiaoxty)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to search recent Gmail messages for job application replies, classify recruiter responses, summarize priority actions, and draft follow-up or reply text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches private Gmail inbox and sent messages through an authenticated gog account.

Mitigation: Confirm the Gmail account and search scope before use, especially on shared or work machines.

Risk: The generated summaries and reply drafts may include sensitive recruiter, employer, or application details.

Mitigation: Review summaries and drafts before sharing or sending, and avoid exposing unnecessary personal or employer information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoxty/skills/email-reply-reader)
- [Publisher profile](https://clawhub.ai/user/xiaoxty)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and reply templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated gog Gmail access to search recent inbox and sent messages.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
