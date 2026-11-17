## Description:

Company Search Fengniao queries Riskbird/Fengniao for Chinese company registration, ownership, management, investment, change-history, credit, and risk records after fuzzy company matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elijah-pi](https://clawhub.ai/user/elijah-pi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to verify Chinese companies, screen counterparties or suppliers, and generate due-diligence reports before business decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names and due-diligence targets are sent to Riskbird.

Mitigation: Install only where sending lookup targets to Riskbird is acceptable, and avoid sensitive or undisclosed counterparty searches unless that data sharing is approved.

Risk: FN_API_KEY may be transmitted as a URL parameter.

Mitigation: Use a public-use or least-privilege key where possible, and avoid using a paid or private key unless URL-parameter secret transport is acceptable.

Risk: Setup checks can expose the full API key on screen.

Mitigation: Verify key presence without printing the full secret, and rotate any key that is displayed or logged.

Risk: Broad auto-invocation can trigger company lookup behavior for general company-search requests.

Mitigation: Review invocation triggers before deployment and confirm the user intended a Riskbird/Fengniao lookup before sending company identifiers.

## Reference(s):

- [Skill page](https://clawhub.ai/elijah-pi/skills/fengniao-search)
- [Riskbird API key and quota page](https://www.riskbird.com/skills)
- [Riskbird website](https://www.riskbird.com/)
- [Production API endpoint](https://m.riskbird.com/prod-qbb-api)
- [Due diligence report guide](references/due_diligence_report.md)
- [Common business information field definitions](references/field_definitions_common_bizinfo.md)
- [Legal field definitions](references/field_definitions_legal.md)
- [Risk field definitions](references/field_definitions_risk.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports, JSON API responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fuzzy company matching before dimension-specific lookup; local CLI usage depends on Node.js and FN_API_KEY or the bundled public key.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
