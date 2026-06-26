## Description: <br>
Anonymize sensitive data in databases, files, and APIs for testing and compliance. Detect PII (names, emails, SSNs, addresses, phone numbers), apply anonymization strategies (masking, hashing, synthetic replacement), and generate realistic fake data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to detect PII, anonymize production-derived datasets, generate realistic test data, and prepare compliance-oriented anonymization reports for non-production or analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example scans and reports can expose sensitive data in chat, logs, shell output, or command history. <br>
Mitigation: Use the skill only on authorized datasets, avoid pasting raw PII into agent conversations, and suppress or redact sensitive output before storing logs or reports. <br>
Risk: Database anonymization examples can irreversibly rewrite records if applied to the wrong target or without sufficient safeguards. <br>
Mitigation: Run against copied snapshots or non-production exports, use least-privilege credentials, take a verified backup, preview affected rows, and execute updates in a transaction where possible. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, SQL, and report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposed commands and snippets that require user review before execution on authorized data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
