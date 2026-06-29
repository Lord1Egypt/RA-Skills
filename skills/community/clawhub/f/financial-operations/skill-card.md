## Description: <br>
Operational workflows for parsing KYC onboarding documents and applying a firm's rules grid to evaluate client risk, missing information, and compliance outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial onboarding and compliance teams use this skill to extract structured KYC information from client packets and apply firm rules to produce risk ratings, document checks, rule outcomes, and dispositions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KYC and compliance outputs may be incomplete or incorrect if applicant documents, screening results, or firm rules are missing or outdated. <br>
Mitigation: Review extracted records, cited rule outcomes, and risk ratings against authoritative firm policies and screening systems before using them in onboarding decisions. <br>
Risk: Onboarding documents are untrusted inputs and may contain prompt-injection attempts or misleading content. <br>
Mitigation: Treat document contents only as data to extract, do not follow embedded instructions or links, and keep sensitive actions under explicit user control. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted KYC records, rule outcome tables, risk ratings, missing-document flags, and compliance dispositions for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
