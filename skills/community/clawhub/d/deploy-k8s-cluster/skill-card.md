## Description:

Guides developers and operators through planning, deploying, validating, and documenting a kubeadm-based Kubernetes cluster on Ubuntu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t2phage](https://clawhub.ai/user/t2phage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to design, execute, troubleshoot, validate, and document a new Kubernetes cluster deployment on Ubuntu hosts using kubeadm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require privileged SSH access to Kubernetes hosts.

Mitigation: Use dedicated hosts, SSH keys or an SSH agent, and tightly scoped deployment accounts instead of broad password-based access.

Risk: Cleanup or reset actions may destroy cluster resources or host state.

Mitigation: Back up or isolate target machines and require explicit user confirmation before cleanup or destroy operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/t2phage/skills/deploy-k8s-cluster)
- [Publisher profile](https://clawhub.ai/user/t2phage)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with structured deployment plans, reports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce architecture designs, deployment plans, validation reports, troubleshooting options, and delivery documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
