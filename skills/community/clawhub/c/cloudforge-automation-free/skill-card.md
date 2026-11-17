## Description: <br>
Cloudforge Automation Free helps agents guide single-cloud infrastructure-as-code workflows with Terraform templates, basic resource configuration, and deployment commands for AWS, GCP, or Azure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize a single cloud infrastructure project, generate Terraform templates, and run deployment, destruction, and state-management workflows for AWS, GCP, or Azure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terraform apply and destroy workflows can make high-impact cloud infrastructure changes. <br>
Mitigation: Use least-privilege cloud credentials and non-production accounts unless the generated Terraform plan has been reviewed. <br>
Risk: Automated destroy behavior can remove cloud resources without adequate confirmation. <br>
Mitigation: Remove or override auto-approved destroy behavior and require explicit confirmation before apply or destroy operations. <br>
Risk: Terraform state files and cloud credentials may expose secrets or sensitive resource details. <br>
Mitigation: Avoid storing or committing Terraform state files or secrets, and use secure state backends and sensitive variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloudforge-automation-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Terraform, HCL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes infrastructure templates and cloud CLI/Terraform command guidance; execution should follow Terraform plan review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
