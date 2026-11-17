## Description:

This skill guides cloud security audits against CIS benchmarks for AWS, Azure, and GCP, including benchmark selection, automated assessment, result interpretation, remediation planning, and continuous compliance monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security engineers, auditors, and platform teams use this skill to assess AWS, Azure, and GCP environments against CIS Foundations Benchmarks, prioritize failed controls, and plan remediation and continuous monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes remediation commands that can change live cloud resources across an account.

Mitigation: Review every remediation command before execution, target only confirmed resources, and require normal change approval for production accounts.

Risk: Using broad credentials for audits can increase exposure if commands are copied directly into operational environments.

Mitigation: Use read-only credentials for assessment work and keep remediation privileges separate from audit credentials.

Risk: Benchmark and provider coverage may not match every environment or compliance requirement.

Mitigation: Verify provider coverage, CIS benchmark versions, and local control mappings before relying on results.

## Reference(s):

- [API Reference: Auditing Cloud with CIS Benchmarks](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/ling-qian/skills/auditing-cis-benchmarks)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/)
- [CIS AWS Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [Prowler](https://github.com/prowler-cloud/prowler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks; optional JSON audit report from the bundled AWS audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit output depends on cloud provider, account or project scope, benchmark version, credentials, and selected reporting options.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
