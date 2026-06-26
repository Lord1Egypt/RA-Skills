## Description: <br>
Integrate Didit Database Validation API to verify personal data against government databases, validate national ID numbers, and perform identity database lookups for Latin American and Spanish identity documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to integrate Didit database validation, call the validation API, and interpret identity match results for supported government and financial database checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send government ID data and personal information to a third-party API. <br>
Mitigation: Confirm consent and legal authority before validation, review Didit's privacy and retention terms, and redact sensitive data from logs. <br>
Risk: The skill requires a Didit API key. <br>
Mitigation: Store DIDIT_API_KEY only in secure environment storage and avoid placing credentials in prompts, source files, or logs. <br>
Risk: Some validation, registration, or credit top-up actions may create paid activity. <br>
Mitigation: Require explicit approval before account registration, credit top-ups, or paid validation calls. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit Database Validation API Reference](https://docs.didit.me/standalone-apis/database-validation) <br>
- [Didit Database Validation Feature Guide](https://docs.didit.me/core-technology/database-validation/overview) <br>
- [Didit Database Validation Supported Countries](https://docs.didit.me/core-technology/database-validation/database-validation-supported-countries) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, TypeScript, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party API request examples and command-line validation output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
