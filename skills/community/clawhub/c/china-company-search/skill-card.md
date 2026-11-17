## Description:

China company search and business registry skill by Fengniao (Riskbird) for KYB, supplier verification, due diligence, corporate risk screening, and counterparty risk checks on Chinese companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinshu001](https://clawhub.ai/user/xinshu001)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, procurement teams, and developers use this skill to look up Chinese company registry data and risk signals before onboarding suppliers, signing contracts, or preparing due diligence summaries.

### Deployment Geography for Use:

Global, for China company registry and risk checks.

## Known Risks and Mitigations:

Risk: Company names, person names used for legal-representative lookups, and Riskbird API keys are sent to Riskbird.

Mitigation: Install only for workflows where this disclosure is acceptable, and use a dedicated low-privilege API key where possible.

Risk: API credentials are passed in URL query parameters and may appear in server, proxy, or diagnostic logs.

Mitigation: Monitor key usage, rotate keys periodically, and avoid using broadly privileged credentials.

Risk: Broad auto-invocation may trigger company-risk lookups from ordinary supplier, contract, address, phone, or email questions.

Mitigation: Review auto-invocation behavior before deployment and disable or scope the skill where external lookups require explicit user intent.

Risk: The built-in public key has a daily quota and may fail when quota is exhausted.

Mitigation: Configure a private FN_API_KEY for reliable use and handle quota exhaustion as a recoverable error.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinshu001/skills/china-company-search)
- [Riskbird](https://www.riskbird.com/)
- [Riskbird skills quota page](https://www.riskbird.com/skills)
- [Due diligence report guide](references/due_diligence_report.md)
- [Common business information field definitions](references/field_definitions_common_bizinfo.md)
- [Legal field definitions](references/field_definitions_legal.md)
- [Risk field definitions](references/field_definitions_risk.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON returned from Riskbird API calls, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May synthesize multi-dimension due diligence reports from supported registry and risk records; unsupported dimensions should be stated explicitly.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
