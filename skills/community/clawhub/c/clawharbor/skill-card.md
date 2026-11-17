## Description:

Delegate tasks to specialized agents via the ClawHarbor API -- research, analysis, content, and data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowpigy](https://clawhub.ai/user/shadowpigy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate natural-language tasks such as market research, data collection, content work, translation, and technical research to ClawHarbor, then present quotes, payment links, and delivered results to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions may include confidential, personal, regulated, credential-adjacent, or business-sensitive information sent to ClawHarbor and human agents.

Mitigation: Submit only task descriptions the user is comfortable sharing externally, and avoid including secrets, credentials, regulated data, or unnecessary personal information.

Risk: The skill presents externally supplied payment links.

Mitigation: Inspect payment links carefully before opening them and keep the complete URL, including any fragment, when presenting it to the user.

Risk: Returned results are external content and may be incorrect, incomplete, or unsafe to use directly.

Mitigation: Treat delivered results as untrusted input and review them before relying on, executing, publishing, or forwarding them.

## Reference(s):

- [ClawHarbor website](https://clawharbor.app)
- [ClawHarbor API documentation](https://clawharbor.app/v1)
- [ClawHub skill listing](https://clawhub.ai/shadowpigy/skills/clawharbor)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Text]

**Output Format:** [Markdown or plain text with API request examples, payment links, and returned task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are plain text from an external service; payment URLs must be presented complete and inspected before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
