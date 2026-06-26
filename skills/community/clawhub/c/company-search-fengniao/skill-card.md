## Description: <br>
Enterprise query and risk-screening skill for Chinese company lookup through Fengniao/Riskbird, covering business registration data, legal representatives, shareholders, executives, outbound investments, registration changes, credit and risk records, and due-diligence report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinshu001](https://clawhub.ai/user/xinshu001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to check Chinese company background, ownership, management, investment, registration-change, and risk information before supplier onboarding, customer review, partnership evaluation, or contract signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, person names used for company lookup, entids, and due-diligence query details are sent to Riskbird/Fengniao. <br>
Mitigation: Use the skill only for queries you are comfortable sharing with Riskbird/Fengniao, and avoid submitting sensitive or confidential business details unless your organization has approved that use. <br>
Risk: The built-in public API key is shared and quota-limited. <br>
Mitigation: Configure a private FN_API_KEY when account control, paid quota, or predictable availability is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xinshu001/company-search-fengniao) <br>
- [Fengniao public API key and quota page](https://www.riskbird.com/skills) <br>
- [Fengniao website](https://www.riskbird.com/) <br>
- [Setup and local validation](artifact/SETUP.md) <br>
- [Due diligence report guide](artifact/references/due_diligence_report.md) <br>
- [Common business information field definitions](artifact/references/field_definitions_common_bizinfo.md) <br>
- [Legal risk field definitions](artifact/references/field_definitions_legal.md) <br>
- [Risk field definitions](artifact/references/field_definitions_risk.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text summaries with JSON tool results from Fengniao/Riskbird API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries may include Chinese company names, person names, entids, and due-diligence details; the skill uses FN_API_KEY when supplied and otherwise falls back to a shared public key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
