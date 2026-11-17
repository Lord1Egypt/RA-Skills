## Description: <br>
Helps agents provide AWS architecture selection, basic cost optimization, and resource inventory guidance for MVP and growth-stage projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, independent builders, and cloud teams use this skill to choose basic AWS services, estimate early-stage costs, inspect existing AWS resources, and identify common cost pitfalls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents itself as read-only while including AWS commands that can create or modify real cloud resources and costs. <br>
Mitigation: Run it only with least-privilege read-only AWS credentials unless intentional remediation or provisioning is needed, and require manual review and confirmation before executing any command. <br>
Risk: Architecture and cost guidance may be incomplete for production, enterprise compliance, or advanced security scenarios. <br>
Mitigation: Have an AWS-qualified reviewer validate recommendations before deployment, especially for security, compliance, migration, and infrastructure-as-code work. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with tables, JSON examples, and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include AWS CLI commands and should be manually reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
