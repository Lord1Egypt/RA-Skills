## Description: <br>
Checks health of AWS EC2 instances and ECS clusters/services by reporting running/stopped counts, CPU/memory metrics, and unhealthy tasks for AWS infrastructure monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yashgkar](https://clawhub.ai/user/yashgkar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to query AWS EC2, ECS, and CloudWatch health data and summarize running/stopped counts, resource metrics, and unhealthy ECS tasks for infrastructure monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AWS access keys and a region, so mishandled credentials could expose account access. <br>
Mitigation: Use temporary credentials or a tightly scoped read-only IAM policy for EC2, ECS, and CloudWatch, and avoid sharing secrets in chat or logs. <br>
Risk: Broad account-wide read access can reveal more infrastructure information than needed. <br>
Mitigation: Prefer least-privilege policies limited to the health checks the skill performs. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/yashgkar/aws-health) <br>
- [ClawHub skill listing](https://clawhub.ai/yashgkar/skills/aws-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with shell command examples and structured AWS health report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports EC2 and ECS health status, CPU and memory metrics, unhealthy task information, and error-handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
