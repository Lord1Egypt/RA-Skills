## Description:

Anonymize sensitive data in databases, files, and APIs for testing and compliance. Detect PII (names, emails, SSNs, addresses, phone numbers), apply anonymization strategies (masking, hashing, synthetic replacement), and generate realistic fake data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and compliance teams use this skill to detect and anonymize sensitive data before using production-like datasets for testing, development, analytics, or compliance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PII detection output can expose sensitive matches.

Mitigation: Run scans only on explicit input paths and redact or limit detection output before sharing it.

Risk: Database update examples could overwrite live records.

Mitigation: Use isolated database copies with backups, transactions, dry runs, and human confirmation before any data-changing command.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with bash, Python, SQL, and report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose data-changing commands; review against isolated copies before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
