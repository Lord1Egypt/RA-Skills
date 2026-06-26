## Description: <br>
Query AWS CloudWatch metrics for ECS, EC2, and RDS resources and return text summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[delbertheihei](https://clawhub.ai/user/delbertheihei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect recent AWS CloudWatch metrics for ECS clusters, EC2 instances, and RDS databases from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks this release as suspicious and calls for review before installation. <br>
Mitigation: Review the skill code before installing or running it, especially on Windows. <br>
Risk: The skill requires AWS credentials to query CloudWatch metrics. <br>
Mitigation: Use narrowly scoped CloudWatch read-only permissions, prefer short-lived credentials or an IAM role, and avoid pasting AWS secrets into prompts. <br>
Risk: Broad AWS or local system privileges would increase the impact of misuse or accidental execution. <br>
Mitigation: Run the skill with the minimum AWS and local permissions needed for metric lookup. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries to stdout with min, max, and average values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY; supports AWS_REGION, metric aliases, period, and time-window configuration.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
