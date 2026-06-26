## Description: <br>
Provides a PSBC enterprise-bank direct-connection interface for balance queries, transaction-detail queries, and payment review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hypersonal](https://clawhub.ai/user/hypersonal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to work with PSBC enterprise banking API parameters and endpoint mappings for account balance, transaction history, and payment approval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill targets banking account access and payment approval without defining credential safeguards or payment confirmation controls. <br>
Mitigation: Use only with a verified banking integration, least-privilege test credentials, secure credential storage, explicit sandbox or transaction limits, and separate human review before any payment action. <br>
Risk: The artifact provides endpoint and credential placeholders but little implementation detail, increasing integration ambiguity. <br>
Mitigation: Review the banking API contract, fill configuration from trusted sources only, and test non-payment operations in a sandbox before enabling payment workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hypersonal/cpef-psbc) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown or configuration/code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes operation names, account and currency parameters, date input, amount input, and endpoint placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
