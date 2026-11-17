## Description:

Provides DevOps, platform engineering, and SRE guidance for provisioning, configuration management, CI/CD, container orchestration, observability, incident response, and developer infrastructure workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and SREs use this skill to plan, review, troubleshoot, and document DevOps workflows across infrastructure, deployments, containers, observability, networking, performance, and operational readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment and infrastructure examples could lead to unintended production changes if copied without review.

Mitigation: Require protected environments, human approvals, reviewed plans, and tightly gated production change workflows.

Risk: Terraform plans, kubeconfig handling, logs, or command output could expose sensitive operational details.

Mitigation: Redact sensitive output, avoid publishing full Terraform plans to pull requests, and scope kubeconfig use to temporary files.

Risk: Unpinned GitHub Actions or container image references could introduce unreviewed supply-chain changes.

Mitigation: Pin GitHub Actions and container images to reviewed immutable versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/devops-engineer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, runbook templates, CI/CD snippets, infrastructure examples, and troubleshooting commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
