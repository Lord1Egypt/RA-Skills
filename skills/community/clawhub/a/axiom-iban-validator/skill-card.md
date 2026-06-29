## Description: <br>
IBAN validator that checks international bank account number format, country-specific length, and mod-97 checksum using pure Python standard-library logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and operations teams use this skill to pre-validate IBAN strings before payment submission, customer data audits, or payment form acceptance. It does not verify account existence, account ownership, BIC/SWIFT data, or payment readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: IBAN checksum validation can confirm format and checksum consistency but cannot prove that an account exists or belongs to a customer. <br>
Mitigation: Use this skill only for local pre-validation; perform account existence, ownership, sanction, and payment-readiness checks through appropriate banking or compliance systems. <br>
Risk: Country coverage is documented inconsistently across the artifact, and unsupported countries return unknown-country errors. <br>
Mitigation: Confirm required countries against the bundled IBAN_LENGTHS table and update or verify coverage before relying on the skill for new regions. <br>
Risk: Release license evidence conflicts with artifact frontmatter. <br>
Mitigation: Confirm the authoritative license before redistribution or commercial use. <br>
Risk: The security guidance recommends reviewing commands before execution. <br>
Mitigation: Inspect shell examples and Python invocations before running them, and execute validation in a controlled environment appropriate for financial data handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-iban-validator) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [Plain text or JSON validation results, with markdown usage examples and Python API guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns validity, country, length, checksum status, formatted IBAN, BBAN, original input, or error details.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
