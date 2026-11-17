## Description:

Queries AWS CloudWatch metrics for ECS, EC2, and RDS resources and returns text summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delbertheihei](https://clawhub.ai/user/delbertheihei)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to query recent AWS CloudWatch metrics for ECS clusters, EC2 instances, and RDS databases and receive concise min, max, and average summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can execute the wrong local script or enable shell execution on Windows around AWS credentials.

Mitigation: Review before installing, run only from a trusted skill directory, and avoid the Windows wrapper path until shell execution and path resolution are fixed.

Risk: The skill requires AWS credentials to query CloudWatch.

Mitigation: Use short-lived or role-based AWS credentials with read-only CloudWatch permissions.

Risk: Users may expect rendered charts from the skill metadata, but the release evidence and security guidance indicate text-only output.

Mitigation: Treat the skill output as text summaries only and do not rely on chart rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/delbertheihei/skills/aws-cloud-watch)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text summaries to stdout with command-line usage and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports min, max, and average values for the requested metric; no chart rendering.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
