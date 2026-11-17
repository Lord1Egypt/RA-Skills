## Description:

Help your owner find jobs on ClawHire by guiding them through profile creation, job search, match review, and recruiter communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[box1d](https://clawhub.ai/user/box1d)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to create or update a ClawHire candidate profile, search active jobs, review matches, and manage recruiter visibility through authenticated ClawHire API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles resumes, candidate profile details, contact information, salary expectations, recruiter visibility, API keys, and notification state.

Mitigation: Use it only with a ClawHire account you trust, avoid including unrelated sensitive data in resumes or profile text, and confirm how the API key and profile data are stored and deleted.

Risk: Candidate profiles can become visible to recruiters when activated.

Mitigation: Require explicit user confirmation before activating a profile or changing recruiter visibility.

Risk: Notification state can be changed by marking messages as read.

Mitigation: Summarize unread notifications first and ask for confirmation before marking notifications read.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/box1d/skills/clawhire-candidate)
- [ClawHire API base URL](https://metalink.cc/clawhire/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown and plain text responses with authenticated API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relays ClawHire server conversation content and summarizes job, profile, match, and notification results for the user.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
