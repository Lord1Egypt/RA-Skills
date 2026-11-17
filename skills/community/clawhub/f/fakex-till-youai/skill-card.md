## Description:

Generates X post drafts from a daily AI digest, captures the user's style and profile preferences, supports draft selection and scheduling, and can either publish through the user's own X API credentials or prepare copy-ready posts for manual publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimmw](https://clawhub.ai/user/zimmw)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a daily AI digest use this skill to turn digest items into X post drafts that match their intended AI persona, style, and reference accounts. It supports manual posting or scheduled automatic publishing after the user selects drafts and times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full automatic mode requires X API credentials and can publish publicly through the user's account.

Mitigation: Use half-automatic mode unless direct publishing is required; when enabling automatic posting, configure credentials outside chat where possible and use least-privilege or test-account credentials.

Risk: Scheduled posts can publish unwanted or incorrect content if selected drafts and posting times are not reviewed.

Mitigation: Review final drafts, source links, and exact scheduled times before authorizing publishing.

Risk: Credential storage and safeguards are not specified in enough detail for automatic posting.

Mitigation: Confirm where secrets are stored before enabling full automatic mode and avoid exposing credentials in conversation.

## Reference(s):

- [follow-builders companion digest skill](https://github.com/zarazhangrui/follow-builders)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text post drafts, schedule details, and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local posting configuration and schedule files when full automatic mode is selected and supported by local scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
