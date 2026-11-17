## Description:

Helps a recruiter or HR owner post jobs, manage openings, search candidates, and review candidate matches on ClawHire.

This skill is ready for commercial/non-commercial use.

## Publisher:

[box1d](https://clawhub.ai/user/box1d)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, headhunters, and HR users use this skill to run ClawHire hiring workflows, including job intake, confirmed job publishing, job management, candidate search, and match review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the owner to provide and remember a ClawHire API key.

Mitigation: Use a revocable, least-privilege API key when available, avoid pasting long-lived secrets into ordinary chat, and rotate or revoke the key if exposure is suspected.

Risk: The skill relays remote ClawHire AI messages, which could include requests unrelated to hiring or requests for sensitive information.

Mitigation: Treat remote messages as untrusted content, continue only with hiring-related requests, and decline or escalate messages that ask for unrelated sensitive information.

Risk: The workflow can automatically mark notifications as read after summarizing them.

Mitigation: Review the notification summary before marking notifications read, especially when unread messages may require action outside the skill.

Risk: Recruiting workflows can involve private candidate and hiring information.

Mitigation: Limit shared candidate details to the workflow need, do not reveal candidate names or phone numbers before both sides agree, and keep final hiring decisions under human control.

## Reference(s):

- [ClawHire API Base URL](https://metalink.cc/clawhire/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/box1d/skills/clawhire-recruiter)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text summaries, short lists or tables, and ClawHire API requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawHire API key; relays ClawHire intake responses to the owner and avoids exposing candidate contact details before both sides agree.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
