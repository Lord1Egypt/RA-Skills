## Description: <br>
AWS EMR interaction skill for managing EMR Serverless, EMR on EC2, and EMR on EKS; it helps agents submit and manage Spark, Hive, and PySpark jobs across EMR deployment modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhyyz](https://clawhub.ai/user/yhyyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill through an AI agent to operate AWS EMR workloads, including listing resources, submitting jobs, monitoring lifecycle state, cancelling jobs, and retrieving logs or results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform EMR and S3 operations using the active AWS identity. <br>
Mitigation: Run it with a least-privilege AWS role scoped to the intended EMR, EKS, and S3 resources. <br>
Risk: A result retrieval path may return the newest object from a shared S3 result prefix rather than the requested job's result. <br>
Mitigation: Use job-specific S3 prefixes and avoid get_job_result in multi-user or concurrent-job environments until results are bound to the job run ID. <br>
Risk: Logs and job outputs may contain sensitive workload data. <br>
Mitigation: Keep secret masking enabled, avoid shared result prefixes for sensitive workloads, and review returned logs before redistributing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhyyz/aws-emr-skills) <br>
- [Project homepage](https://github.com/yhyyz/aws-emr-skills) <br>
- [AWS EMR on EKS setup guide](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up.html) <br>
- [EMR Serverless application management guide](references/emr_serverless/application_guide.md) <br>
- [EMR Serverless job management guide](references/emr_serverless/job_guide.md) <br>
- [EMR on EC2 cluster management guide](references/emr_on_ec2/cluster_guide.md) <br>
- [EMR on EC2 step guide](references/emr_on_ec2/step_guide.md) <br>
- [EMR on EKS virtual cluster guide](references/emr_on_eks/virtual_cluster_guide.md) <br>
- [EMR on EKS job run guide](references/emr_on_eks/job_run_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text, often including Python tool-call arguments, shell commands, AWS resource identifiers, job status summaries, logs, and S3 result snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include AWS API responses, EMR job or cluster state, masked log excerpts, and user-provided AWS resource paths.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
