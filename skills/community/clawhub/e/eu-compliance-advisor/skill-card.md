## Description: <br>
A Chinese-language EU trade compliance advisor for Chinese cross-border sellers that routes VAT, EPR compliance, and certificate-verification questions to the eu-compliance-skill plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luongkim20222022-crypto](https://clawhub.ai/user/luongkim20222022-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese cross-border sellers, marketplace operators, and their agents use this skill to receive Chinese-language advisory guidance on EU VAT, IOSS thresholds, EPR obligations, and certificate checks before seeking official registration or professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compliance and tax outputs may be incomplete or outdated for a seller's specific filing situation. <br>
Mitigation: Treat responses as advisory and verify official registration, tax, and product-compliance requirements with the relevant authority or a qualified professional. <br>
Risk: Certificate verification may involve sensitive business documents or certificate text. <br>
Mitigation: Review the separate eu-compliance-skill plugin and avoid submitting sensitive certificates or business documents unless the deployment environment is approved for that data. <br>
Risk: Generic price questions may trigger VAT calculation when the user intended a different pricing task. <br>
Mitigation: Ask for clarification before VAT calculation when the country, transaction type, or compliance intent is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luongkim20222022-crypto/eu-compliance-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls] <br>
**Output Format:** [Chinese markdown-style advisory text with structured lists and plugin-routed compliance results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tax amounts are expected to use euro values with two decimal places when VAT calculation results are returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
