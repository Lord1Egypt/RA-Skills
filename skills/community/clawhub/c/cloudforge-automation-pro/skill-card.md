## Description:

Cloudforge Automatio helps teams and enterprises plan multi-cloud infrastructure-as-code workflows across Terraform, Ansible, CloudFormation, CI/CD, compliance auditing, disaster recovery, cost optimization, and security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and cloud architects use this skill to draft cloud infrastructure automation plans, configuration snippets, CI/CD deployment flows, compliance checks, disaster recovery runbooks, cost optimization steps, and security hardening guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward cloud infrastructure changes that affect real resources.

Mitigation: Use scoped cloud credentials, explicit account and region boundaries, and non-production defaults until changes are reviewed.

Risk: Examples include apply-style Terraform and Ansible execution paths.

Mitigation: Require plan-only previews, protected CI/CD environments, and manual approval before any Terraform apply or Ansible execution.

## Reference(s):

- [Cloudforge Automatio on ClawHub](https://clawhub.ai/thcjp/skills/cloudforge-automation-pro)
- [Publisher profile: thcjp](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with infrastructure code, YAML, HCL, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud deployment plans, compliance checklists, runbooks, and command examples that require human review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
