## Description: <br>
AWS ECS production health monitoring with CloudWatch log analysis - monitors ECS service health, ALB targets, SSL certificates, and provides deep CloudWatch log analysis for error categorization, restart detection, and production alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briancolinger](https://clawhub.ai/user/briancolinger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to monitor AWS ECS production services, inspect ECS and ALB health, check SSL expiry, and analyze CloudWatch logs for failure patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads production ECS service state, ELB target health, and CloudWatch logs through the configured AWS CLI profile. <br>
Mitigation: Use a dedicated read-only AWS role scoped to the intended region, cluster, services, target groups, and log groups. <br>
Risk: Automatic service discovery and one load-balancer check can inspect resources beyond the intended service set. <br>
Mitigation: Set ECS_SERVICES explicitly and verify the target cluster, service list, and log-group pattern before running diagnostics. <br>
Risk: Generated health and log reports may contain operational details from production systems. <br>
Mitigation: Write reports to a protected directory and restrict access to generated health, alert, and log-analysis files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON health or log report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AWS CLI profile with access to the target ECS cluster, load balancer data, and CloudWatch logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
