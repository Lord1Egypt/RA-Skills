## Description:

Code-Right creates hosted software copyright application material generation tasks that produce formatted Word documents, browser screenshots, ZIP packages, and email download links from a system name and recipient email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyiyu](https://clawhub.ai/user/ziyiyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to submit a software system name and notification email for automated software copyright application material generation. The hosted workflow returns a task identifier and later sends generated materials to the requested recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the system name, recipient email, optional system description, and optional access token to softcraft.cloud for hosted processing.

Mitigation: Install only if hosted processing is approved, avoid confidential system details unless permitted, and provide an access token only when authenticated filtering or protected downloads are needed.

Risk: Generated material download details are sent to the supplied email address.

Mitigation: Double-check the notification email before creating a task.

## Reference(s):

- [Code-Right homepage](https://softcraft.cloud)
- [ClawHub skill page](https://clawhub.ai/ziyiyu/skills/code-right-skill)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Files]

**Output Format:** [JSON task response with hosted document, screenshot, ZIP, and email delivery side effects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a system name and notification email; optional system description and access token may be provided.]

## Skill Version(s):

0.2.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
