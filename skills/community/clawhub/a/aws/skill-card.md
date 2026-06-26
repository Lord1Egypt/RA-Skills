## Description: <br>
Architect, deploy, and optimize AWS infrastructure avoiding cost explosions and security pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and technical operators use this skill for AWS architecture guidance, service selection, deployment planning, cost optimization, and security hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact AWS commands can change infrastructure, IAM, budgets, logging, data retention, and costs. <br>
Mitigation: Before execution, verify AWS_PROFILE, account ID, region, resource names, and whether the command creates, changes, deletes, grants access, changes retention, or affects costs; require explicit approval for those actions. <br>
Risk: AWS CLI guidance can operate against the wrong local credentials, account, or region if context is not checked first. <br>
Mitigation: Confirm caller identity, profile, account type, region, and target resources before proposing or running operations. <br>
Risk: AWS resources and defaults can create ongoing spend through idle load balancers, NAT traffic, snapshots, logs, and oversized instances. <br>
Mitigation: Include cost impact, budget alerts, smallest viable resources, retention policies, lifecycle cleanup, and review steps in recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/aws) <br>
- [Skill homepage](https://clawic.com/skills/aws) <br>
- [Setup guide](setup.md) <br>
- [Service patterns](services.md) <br>
- [Cost optimization](costs.md) <br>
- [Security hardening](security.md) <br>
- [Memory template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose AWS CLI, Terraform, or CloudFormation snippets; execution requires user review and approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
