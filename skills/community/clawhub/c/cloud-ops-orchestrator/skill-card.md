## Description:

云运维编排器 helps agents plan, review, and guide Terraform and Ansible workflows for multi-cloud infrastructure operations, including drift detection, environment isolation, credential handling, and guarded destroy procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, DevOps engineers, and automation teams use this skill to structure multi-cloud IaC operations across AWS, GCP, and Azure with Terraform for resource lifecycle changes and Ansible for host configuration. It is intended to support plan-review-apply workflows, drift checks, environment separation, rollback guidance, and guarded destroy procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad execution and write authority around Terraform, Ansible, cloud CLIs, and cloud credentials.

Mitigation: Use it only in repositories and cloud accounts where the agent is explicitly authorized to run these tools, with least-privilege cloud roles and isolated credentials.

Risk: The safety gates for plan, apply, reconcile, and destroy are described in documentation but are not enforceable code in this artifact.

Mitigation: Require human review and explicit approval for plan, apply, reconcile, and destroy actions, especially in production.

Risk: Infrastructure changes can affect production resources or expose credentials if applied in the wrong environment.

Mitigation: Keep environment state and credentials separated, avoid committing secrets, and review target environment, state backend, and cloud identity before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cloud-ops-orchestrator)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell, Terraform, Ansible, JSON, YAML, and HCL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed by a human before applying infrastructure changes, especially plan, apply, reconcile, and destroy actions.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
