## Description:

Systematically audits AWS S3 bucket permissions to identify publicly accessible buckets, overly permissive ACLs, misconfigured bucket policies, and missing encryption settings using AWS CLI, S3audit, and Prowler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, cloud administrators, and compliance reviewers use this skill to audit AWS S3 bucket exposure, access controls, encryption, versioning, and logging posture. It supports baseline assessments, incident response, and periodic compliance reviews for AWS storage environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow mixes read-only audit steps with commands that create IAM Access Analyzers or modify S3 bucket settings.

Mitigation: Use read-only AWS credentials for assessment steps and require explicit approval plus change-management review before running Access Analyzer creation or S3 put-* remediation commands in production.

Risk: The workflow relies on third-party tools such as Prowler and S3audit.

Mitigation: Pin tool versions, install them in an isolated environment, and review their configuration before running them against production AWS accounts.

Risk: Generated audit reports can contain account identifiers, bucket names, policy details, and security findings.

Mitigation: Store reports in approved locations, restrict access to authorized reviewers, and avoid sharing raw output outside the assessment team.

## Reference(s):

- [API Reference: Auditing AWS S3 Bucket Permissions](references/api-reference.md)
- [boto3 S3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [AWS S3 security documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html)
- [ClawHub skill page](https://clawhub.ai/ling-qian/skills/auditing-aws-s3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python examples; JSON audit reports from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can write an S3 audit report JSON file containing account, bucket, finding, and risk-level details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
