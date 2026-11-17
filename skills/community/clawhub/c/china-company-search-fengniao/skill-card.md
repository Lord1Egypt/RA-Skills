## Description:

China company search and business registry skill by Fengniao (Riskbird) for KYB, supplier verification, company due diligence, corporate risk screening, and counterparty risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elijah-pi](https://clawhub.ai/user/elijah-pi)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, onboarding, procurement, and business development teams use this skill to look up Chinese companies, verify suppliers, screen counterparties, and generate due diligence summaries from Fengniao/Riskbird data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company or person-related lookup terms are sent to a third-party Riskbird API.

Mitigation: Use the skill only for queries you are permitted to share with Riskbird and avoid entering unnecessary sensitive details.

Risk: Private FN_API_KEY values are sent as URL query parameters, which can be exposed in logs or request history.

Mitigation: Use a low-privilege API key where possible, restrict log access, and rotate the key if exposure is suspected.

Risk: The included public API key has shared daily quota limits.

Mitigation: Configure a private FN_API_KEY for production workflows or retry after quota reset when public quota is exhausted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elijah-pi/skills/china-company-search-fengniao)
- [Riskbird skills and quota page](https://www.riskbird.com/skills)
- [Riskbird website](https://www.riskbird.com/)
- [Due diligence report guide](references/due_diligence_report.md)
- [Common business information field definitions](references/field_definitions_common_bizinfo.md)
- [Legal field definitions](references/field_definitions_legal.md)
- [Risk field definitions](references/field_definitions_risk.md)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown summaries and structured API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include due diligence report sections, registry fields, legal and risk record summaries, or no-record/not-supported statements based on returned data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
