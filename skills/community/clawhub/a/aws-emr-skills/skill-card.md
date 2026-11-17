## Description:

AWS EMR interaction skill for managing EMR Serverless, EMR on EC2, and EMR on EKS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhyyz](https://clawhub.ai/user/yhyyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage AWS EMR Serverless, EMR on EC2, and EMR on EKS resources through an agent, including submitting Spark, Hive, and PySpark jobs, checking status, retrieving logs, and managing resource lifecycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make impactful AWS changes, including job submission, cancellation, cluster termination, and virtual-cluster deletion.

Mitigation: Use least-privilege AWS credentials, test in a non-production account first, and require explicit confirmation before mutating AWS resources.

Risk: One result-retrieval path may return data from the wrong job when shared S3 result prefixes are used.

Mitigation: Avoid shared S3 result prefixes for result retrieval until results are bound to exact job IDs.

Risk: Unpinned installer or dependency versions can introduce unexpected behavior.

Mitigation: Pin installer and dependency versions before deployment.

## Reference(s):

- [AWS EMR Skills Homepage](https://github.com/yhyyz/aws-emr-skills)
- [EMR on EKS setup documentation](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up.html)
- [EMR Serverless application management guide](references/emr_serverless/application_guide.md)
- [EMR Serverless job guide](references/emr_serverless/job_guide.md)
- [EMR on EC2 cluster guide](references/emr_on_ec2/cluster_guide.md)
- [EMR on EC2 step guide](references/emr_on_ec2/step_guide.md)
- [EMR on EKS virtual cluster guide](references/emr_on_eks/virtual_cluster_guide.md)
- [EMR on EKS job run guide](references/emr_on_eks/job_run_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline code, shell commands, and structured AWS operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate AWS EMR, EMR Serverless, EMR Containers, and S3 API operations when used with configured AWS credentials.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
