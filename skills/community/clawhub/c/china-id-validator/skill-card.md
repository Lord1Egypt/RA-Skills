## Description: <br>
Validate Chinese mainland ID card numbers, extract province, birth date, gender, and age, convert between 15- and 18-digit formats, and verify 18-digit checksums. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to validate, parse, and transform Chinese mainland ID card numbers in local workflows. It can also generate controlled test ID values for validation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real Chinese ID numbers are sensitive personal data and may appear in terminal output or chat logs. <br>
Mitigation: Avoid entering real ID numbers unless necessary, and handle any output or logs as sensitive data. <br>
Risk: The included ID generator could be misused for account creation, KYC bypass, or real-world identity workflows. <br>
Mitigation: Use generated IDs only as controlled test data and do not use them for real-world identity or eligibility decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/china-id-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON objects printed by the local CLI, with optional Markdown guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and returns validation status, extracted attributes, conversion output, errors, or generated test IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
