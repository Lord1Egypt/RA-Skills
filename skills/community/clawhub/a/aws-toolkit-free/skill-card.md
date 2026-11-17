## Description: <br>
Aws Toolkit Free helps agents provide basic AWS deployment and resource-management guidance for EC2 instances, S3 buckets, VPC networks, security groups, and IAM basics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent draft basic AWS resource-management commands, configuration steps, and operational guidance for small deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to operate AWS resources from local credentials, including destructive resource changes and IAM, security group, or VPC updates. <br>
Mitigation: Use a least-privilege IAM profile, avoid root or broad administrator keys, keep secrets out of prompts and logs, and require explicit confirmation before create, delete, stop, IAM, security group, or VPC changes. <br>
Risk: The security summary reports overly broad activation wording and weak guardrails for destructive AWS changes. <br>
Mitigation: Use the skill only for explicit AWS EC2, S3, VPC, security group, or IAM basics requests, and route vague or unrelated coding and deployment tasks to a more specific workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured status, result, execution log, and error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
