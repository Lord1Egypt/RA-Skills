## Description: <br>
China company search and business registry skill by Fengniao (Riskbird) for KYB, supplier verification, company due diligence, corporate risk screening, and counterparty risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elijah-pi](https://clawhub.ai/user/elijah-pi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, procurement, onboarding, and business teams use this skill to look up Chinese companies, verify suppliers, screen counterparties, and produce concise due diligence reports from Fengniao/Riskbird data. <br>

### Deployment Geography for Use: <br>
Global; data coverage is focused on Chinese companies. <br>

## Known Risks and Mitigations: <br>
Risk: Company names, person names, entity IDs, and due-diligence queries are sent to the external Riskbird/Fengniao API. <br>
Mitigation: Use the skill only when that external sharing is acceptable, and avoid submitting highly confidential target lists unless the provider is trusted for the workflow. <br>
Risk: The built-in public API key has a daily quota and private API keys are passed to the provider for requests. <br>
Mitigation: Configure a private FN_API_KEY for production use, monitor quota errors, and treat the key as a credential. <br>
Risk: Fuzzy search can return multiple Chinese company matches, and choosing the wrong entity can produce an incorrect due diligence result. <br>
Mitigation: Confirm the official registered company before querying detailed dimensions, especially for abbreviated or ambiguous names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elijah-pi/china-company-search-fengniao) <br>
- [Riskbird Fengniao Skills](https://www.riskbird.com/skills) <br>
- [Riskbird](https://www.riskbird.com/) <br>
- [Setup Guide](SETUP.md) <br>
- [Due Diligence Report Guide](references/due_diligence_report.md) <br>
- [Common Business Information Field Definitions](references/field_definitions_common_bizinfo.md) <br>
- [Legal Field Definitions](references/field_definitions_legal.md) <br>
- [Risk Field Definitions](references/field_definitions_risk.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and concise text summaries, with optional shell command examples for local tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Chinese company names for fuzzy search; detailed lookups require the resolved company entity ID internally and may require FN_API_KEY when public quota is exhausted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
