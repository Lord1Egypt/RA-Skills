## Description: <br>
Systematically audits AWS S3 bucket permissions to identify publicly accessible buckets, overly permissive ACLs, misconfigured bucket policies, and missing encryption settings using AWS CLI, S3audit, and Prowler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, cloud platform teams, and compliance reviewers use this skill to assess S3 buckets for public access, broad bucket policies, missing encryption, missing versioning, and related data-protection gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes remediation snippets that can make live AWS S3 configuration changes. <br>
Mitigation: Run read-only checks first, confirm each bucket's intended access model, and route put-* AWS CLI or boto3 changes through normal production change control. <br>
Risk: Auditing production buckets with broad credentials can expose sensitive cloud inventory and access data. <br>
Mitigation: Use authorized AWS credentials with the least privilege needed for the scoped accounts and buckets, and handle generated reports as security-sensitive artifacts. <br>
Risk: Blocking public access can interrupt intended static websites, CloudFront origins, partner integrations, or other public delivery paths. <br>
Mitigation: Validate bucket ownership, dependencies, and exception cases before applying public-access, encryption, KMS, or versioning changes. <br>


## Reference(s): <br>
- [API Reference: Auditing AWS S3 Bucket Permissions](references/api-reference.md) <br>
- [boto3 S3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) <br>
- [Amazon S3 security documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security.html) <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/auditing-aws-s3) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash and Python examples; optional JSON audit report from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke AWS CLI, boto3, Prowler, S3audit, or IAM Access Analyzer with authorized AWS credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
