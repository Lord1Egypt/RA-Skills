## Description: <br>
Surfaces up to three ClawHub skill recommendations for e-commerce agents across platforms, order management, inventory, payments, support, and peak-season workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicope](https://clawhub.ai/user/nicope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to audit an e-commerce agent's mission, search ClawHub for relevant skills, score candidates, and produce a short recommendation report before onboarding, weekly reviews, or peak-season preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads SOUL.md and writes a local recommendation report, which could expose sensitive agent context if secrets or customer details are present. <br>
Mitigation: Keep API keys, customer PII, payment details, and sensitive operational data out of SOUL.md and generated reports. <br>
Risk: E-commerce agents may handle payments, customer PII, and inventory write access, so weak skill recommendations can have higher operational impact. <br>
Mitigation: Run a security audit before installing recommended skills and verify platform compatibility, order-volume constraints, security status, and existing installations. <br>
Risk: Recommendations are based on public ClawHub searches and may miss newly released, private, or renamed skills. <br>
Mitigation: Review the final top 3 manually against current operational needs before installation. <br>


## Reference(s): <br>
- [Clawtrix Ecom Intel on ClawHub](https://clawhub.ai/nicope/clawtrix-ecom-intel) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown recommendation report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits recommendations to the top 3 and may persist the report under memory/reports.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
