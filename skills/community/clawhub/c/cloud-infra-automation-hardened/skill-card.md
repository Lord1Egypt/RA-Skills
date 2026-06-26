## Description: <br>
Automate cloud infrastructure provisioning and management via IaC tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to plan and manage AWS, Google Cloud Platform, and Azure infrastructure with Terraform, Ansible, CloudFormation, and related cloud CLIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud apply or destroy operations can change or remove production infrastructure. <br>
Mitigation: Review the plan first, call out resources marked for destruction or replacement, and require explicit confirmation naming the target environment before destructive commands. <br>
Risk: An agent could access or modify cloud resources outside the intended account, project, or subscription. <br>
Mitigation: Limit actions to explicitly named cloud scopes and verify the account, project, subscription, profile, and credentials before running commands. <br>
Risk: Terraform state, cloud CLI output, and resource metadata can contain secrets or sensitive infrastructure details. <br>
Mitigation: Do not pipe raw state or cloud resource output to external endpoints; use local analysis, sanitized summaries, or approved secure transfer paths when needed. <br>
Risk: The referenced local ./cloud.sh helper was not included in the reviewed artifact. <br>
Mitigation: Inspect the local script before execution and confirm that its behavior matches the intended account, environment, and operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/cloud-infra-automation-hardened) <br>
- [Faberlens cloud infrastructure automation safety evaluation](https://faberlens.ai/explore/cloud-infra-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline shell commands and infrastructure-as-code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud command plans, IaC configuration guidance, deployment pipeline steps, and safety checks before apply or destroy operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
