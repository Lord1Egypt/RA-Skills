## Description: <br>
This skill details how to conduct cloud security audits using Center for Internet Security benchmarks for AWS, Azure, and GCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, cloud platform teams, and auditors use this skill to assess AWS, Azure, and GCP environments against CIS Foundations Benchmarks, interpret failed controls, and plan remediation and continuous compliance monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remediation commands can change production cloud accounts if copied without review. <br>
Mitigation: Replace placeholders, scope target resources, test changes outside production, obtain change approval, and prepare rollback steps before applying remediation. <br>
Risk: The AWS audit helper uses cloud credentials and reads account configuration through provider APIs. <br>
Mitigation: Run the helper only with scoped read-only audit credentials and avoid using remediation privileges during assessment. <br>
Risk: Audit findings and generated reports may expose sensitive cloud configuration details. <br>
Mitigation: Store reports in access-controlled locations and share them only with teams responsible for security review and remediation. <br>


## Reference(s): <br>
- [API Reference: Auditing Cloud with CIS Benchmarks](references/api-reference.md) <br>
- [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/) <br>
- [CIS Benchmarks for Amazon Web Services](https://www.cisecurity.org/benchmark/amazon_web_services) <br>
- [Prowler](https://github.com/prowler-cloud/prowler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON audit reports when using the included AWS helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
