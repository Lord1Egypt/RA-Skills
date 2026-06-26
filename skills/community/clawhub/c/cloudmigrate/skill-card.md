## Description: <br>
Automate multi-cloud migrations and infrastructure deployments with customizable IaC workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and cloud platform teams use this skill to plan migrations, generate infrastructure-as-code, prepare deployment workflows, and produce validation or rollback procedures across AWS, Azure, GCP, and hybrid environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request broad cloud credentials and generate infrastructure-changing actions. <br>
Mitigation: Use sandbox or least-privilege temporary credentials, scoped to only the cloud provider needed for the task. <br>
Risk: Generated infrastructure-as-code or commands could deploy, delete, modify resources, or incur cloud costs. <br>
Mitigation: Inspect all generated IaC and commands before use, and require explicit confirmation before any apply, deploy, delete, or cost-incurring operation. <br>


## Reference(s): <br>
- [Cloudmigrate on ClawHub](https://clawhub.ai/ncreighton/cloudmigrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command snippets, configuration examples, and structured migration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include infrastructure-as-code, cloud CLI commands, deployment plans, cost estimates, risk assessments, and rollback procedures for human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
