## Description:

Process browser-extension webhook messages prefixed with [Clawfy Pro] by using the included URL, page context, and recent conversation context to identify the user's task, offer targeted help, and suggest relevant ClawHub skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vabblejames](https://clawhub.ai/user/vabblejames)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn browser page context and recent conversation context into task-aware assistance and ClawHub skill recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser page text and recent conversation context to generate assistance and recommendations.

Mitigation: Install only when this data flow is acceptable, and avoid using the extension on pages or conversations containing sensitive information.

Risk: The skill suggests ClawHub skills and install commands that could lead users to install untrusted packages.

Mitigation: Review each suggested skill, publisher, and command before running any installation.

## Reference(s):

- [Clawfy Pro on ClawHub](https://clawhub.ai/vabblejames/skills/clawfy-pro)
- [Publisher profile](https://clawhub.ai/user/vabblejames)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with suggested ClawHub links and install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include a connection or new-topic classification, direct help offers, ranked skill suggestions, and per-skill relevance explanations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
