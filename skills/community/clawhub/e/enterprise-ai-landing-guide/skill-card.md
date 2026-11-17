## Description:

Helps an enterprise identify one AI use case that can be validated within seven days through up to six dynamic questions, then optionally request Blueprint FDE human review after separate user consents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yliu35126-afk](https://clawhub.ai/user/yliu35126-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and consultants use this skill to turn a known business problem or lightweight AI opportunity scan into one prioritized AI landing map with validation steps, retained human responsibilities, stop conditions, and an optional human review request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send sensitive business data and session tokens to an unvalidated endpoint if the API base environment variable is overridden.

Mitigation: Review before installing, use only a trusted HTTPS production endpoint, avoid overriding ENTERPRISE_AI_LANDING_API_BASE unless you control the target service, and require endpoint validation before deployment.

Risk: Contact details may be transmitted even when the user has not explicitly consented to being contacted.

Mitigation: Do not pass contact names, phone numbers, or email addresses unless the user has explicitly agreed to be contacted; suppress or reject contact fields when contact consent is false.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yliu35126-afk/skills/enterprise-ai-landing-guide)
- [Skill homepage](https://fde.lantuzhigou.com/enterprise-ai-landing-guide)
- [Public OpenAPI](https://fde.lantuzhigou.com/api/public/clawhive/v1/openapi.yaml)
- [API contract](references/API.md)
- [Output guide](references/OUTPUT.md)
- [Usage boundaries](references/usage-boundaries.md)
- [Privacy and data handling](PRIVACY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured JSON, with optional shell commands for API interaction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a prioritized AI landing map with facts, evidence, inferences, pending confirmations, 7-day validation steps, 30-day indicators, stop conditions, and optional FDE human review status.]

## Skill Version(s):

1.2.0 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
