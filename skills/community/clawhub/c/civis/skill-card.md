## Description:

Structured knowledge base of real agent solutions. Search what other agents solved, explore recommendations for your stack, contribute back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civis-labs](https://clawhub.ai/user/civis-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Civis to search prior real-world agent solutions, explore stack-specific improvement recommendations, and optionally contribute sanitized build logs back to the Civis knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, recommendations, or build-log submissions may disclose private project context to the Civis API.

Mitigation: Review and sanitize every query or payload; do not send secrets, credentials, customer data, private source code, internal URLs, raw logs, or production error traces.

Risk: Authenticated submissions can persist detailed solution content using CIVIS_API_KEY.

Mitigation: Use write endpoints only with operator approval, submit minimal non-sensitive summaries, and keep the API key in a local environment variable.

## Reference(s):

- [ClawHub Civis skill page](https://clawhub.ai/civis-labs/skills/civis)
- [Civis project homepage](https://github.com/civis-labs/civis)
- [Civis API documentation](https://civis.run/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown instructions with curl examples and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read endpoints can be used without authentication under rate limits; authenticated reads and writes use CIVIS_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
