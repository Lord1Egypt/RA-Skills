## Description:

Queries Amazon competitor data through the ClawEC API by brand, seller, ASIN, or keyword, with optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to look up Amazon competitor data, review BSR, sales, price, top brands, and optionally request an AI-generated interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon competitor research inputs and account log lookups are sent to ClawEC using CLAWEC_API_KEY.

Mitigation: Install only if this data sharing is acceptable, prefer a dedicated API key, and avoid submitting sensitive inputs.

Risk: API usage may depend on ClawEC account costs, credits, or retention expectations.

Mitigation: Review ClawEC account cost and retention expectations before deployment.

Risk: The skill interface and source instructions are primarily Chinese.

Mitigation: Ensure operators can review Chinese prompts and results, or provide translation before acting on generated analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-competitor-monitor)
- [ClawEC API Base URL](https://www.clawec.com/api)
- [ClawEC API Key Page](https://www.clawec.com/api-key?source=q-clawhub)
- [ClawEC Signup Page](https://www.clawec.com/?source=q-clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include competitor lists, BSR, sales, price, top brands, AI analysis, request status, and timeout status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
