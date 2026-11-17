## Description:

Analyzes Amazon ASIN advantage through the ClawEC API, including ASIN details, sales trends, sales forecasts, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to request ClawEC ASIN advantage analysis for supported marketplaces and review details, sales trends, forecasts, and optional AI interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASIN research queries and related parameters are sent to ClawEC using the user's ClawEC API key.

Mitigation: Use a dedicated or revocable API key and store it in CLAWEC_API_KEY or a secret manager.

Risk: History and detail helpers can access ClawEC ASIN search logs for the authenticated account.

Mitigation: Run log history and detail helpers only when the agent is expected to inspect those ASIN search logs.

Risk: Authentication, token, or quota failures can prevent analysis from completing.

Mitigation: Check returned status and business codes, including invalid-token and insufficient-points responses, before presenting results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-asin-advantage)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ASIN details, sales trend tables, sales forecast data, AI interpretation text, log IDs, and asynchronous polling status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
