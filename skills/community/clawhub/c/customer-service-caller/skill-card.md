## Description:

Polly calls customer service for the user, navigating phone menus, waiting on hold, explaining the issue, and pursuing a resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-yox](https://clawhub.ai/user/hi-yox)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to delegate customer-service phone calls and incoming-call handling to PollyReach, including refunds, cancellations, billing corrections, reservations, and message summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive call data, including transcripts, recordings, caller numbers, account issues, and other personal or business communications.

Mitigation: Use the skill only with explicit user approval for each call or polling setup, and treat transcripts, recordings, caller numbers, and related summaries as sensitive data.

Risk: The skill stores and reuses a PollyReach service token.

Mitigation: Keep the token file private, limit access to the configured PollyReach key file, and remove or rotate the token when access is no longer needed.

Risk: The skill encourages public sharing of the assigned phone number.

Mitigation: Share the assigned number only with an appropriate privacy notice and a reviewed inbound-answering prompt.

Risk: The skill can produce full transcript, recording-link, and promotional referral output by default.

Mitigation: Review generated call reports before sharing them and omit sensitive or promotional content when it is not appropriate for the audience.

## Reference(s):

- [Customer Service Caller on ClawHub](https://clawhub.ai/hi-yox/skills/customer-service-caller)
- [PollyReach homepage](https://pollyreach.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain-text task updates with shell command invocations and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include call status, transcripts, recordings, caller numbers, credit balance, and PollyReach account or activation status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
