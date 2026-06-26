## Description: <br>
Company Search Fengniao helps agents look up Chinese company registry, ownership, management, investment, change-history, credit, enforcement, abnormal-operation, serious-illegal, and administrative-penalty data through Riskbird/Fengniao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elijah-pi](https://clawhub.ai/user/elijah-pi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill for company due diligence, supplier verification, counterparty background checks, and pre-contract risk screening for Chinese businesses. The skill first resolves a company by name, then queries supported business-information and risk dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Company names, person-name lookup terms, entid values, and FN_API_KEY values are sent to Riskbird. <br>
Mitigation: Use the skill only for lookups that may be shared with Riskbird, and prefer a dedicated API key with appropriate account controls. <br>
Risk: The API key is passed as a URL parameter, which can be exposed through terminal output, logs, proxies, or request tracing. <br>
Mitigation: Avoid printing full request URLs, avoid sharing command transcripts that contain credentials, and rotate the API key if it may have been logged. <br>
Risk: Broad business-background prompts may invoke the skill automatically and trigger external API calls. <br>
Mitigation: Review prompts before execution when handling sensitive company or person-name queries, and disable or constrain auto-invocation where policy requires explicit approval. <br>
Risk: The built-in public API key has daily quota limits and may fail when the shared quota is exhausted. <br>
Mitigation: Configure a private FN_API_KEY for reliable use and treat quota failures as service-limit events rather than local configuration errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elijah-pi/fengniao-search) <br>
- [Riskbird skills page](https://www.riskbird.com/skills) <br>
- [Riskbird website](https://www.riskbird.com/) <br>
- [Due diligence report guide](references/due_diligence_report.md) <br>
- [Common business-information field definitions](references/field_definitions_common_bizinfo.md) <br>
- [Legal field definitions](references/field_definitions_legal.md) <br>
- [Risk field definitions](references/field_definitions_risk.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-backed lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish Riskbird structured data from any supplemental public web information and should not expose internal entid values to end users.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
