## Description:

Judges whether an email is important or urgent by triaging subject and sender signals, checking technical authentication evidence, and analyzing content for phishing or action risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shingo0620](https://clawhub.ai/user/shingo0620)

### License/Terms of Use:


## Use Case:

Employees and other email users use this skill to decide whether a message should be ignored, escalated, or handled carefully. It helps produce an advisory priority, risk level, and safe next action for emails that may involve money, account access, downloads, sensitive data, or social engineering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The triage result is advisory and may miss nuance, especially when only subject and sender signals are available or when messages are outside the examples emphasized by the skill.

Mitigation: Verify sensitive requests through official channels, avoid email links for account or payment actions, and review headers, authentication alignment, links, and attachments when escalation is warranted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown triage summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory priority, technical-verdict, risk-level, and next-step recommendations for a single email-analysis workflow.]

## Skill Version(s):

1.0.1 (source: server evidence release and artifact CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
