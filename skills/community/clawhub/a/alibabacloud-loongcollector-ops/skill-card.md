## Description:

Alibaba Cloud LoongCollector / SLS installation, collection onboarding, Pipeline config management and validation, machine groups, permission troubleshooting, and Lens queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and cloud operations teams use this skill to plan, validate, and execute Alibaba Cloud LoongCollector and SLS installation, onboarding, configuration, machine-group, permission, and Lens-query workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide remote host, ECS, ACK, Kubernetes, and SLS changes that may affect production infrastructure.

Mitigation: Review the plan before execution, use a least-privilege Alibaba Cloud profile, run preflight checks, and require explicit approval before reversible, high-impact, or destructive changes.

Risk: Server security evidence reports unsafe shell command construction risk in generated operational flows.

Mitigation: Do not run host or ECS install flows until rendered commands strictly validate and shell-quote all parameters; inspect commands before execution.

Risk: Installer downloads and ACK role creation can introduce supply-chain or privilege-expansion risk.

Mitigation: Pin and verify installer downloads, and narrow or approve ACK role creation role-by-role before use.

Risk: Operational troubleshooting may expose credentials, kubeconfig contents, SSH keys, or cloud account details.

Mitigation: Never paste secrets, kubeconfig contents, SSH keys, or raw credential files into chat; rely on configured profiles and redacted outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-loongcollector-ops)
- [Skill instructions](SKILL.md)
- [Prerequisites and preflight gates](references/prerequisites.md)
- [Risk levels, approval, snapshot, and rollback](references/risk-and-approval.md)
- [RAM policies](references/ram-policies.md)
- [Pipeline config model](references/pipeline-config.md)
- [ACK install guide](references/install-ack.md)
- [SLS Lens contracts](references/sls-lens-contracts.md)
- [Pipeline templates](assets/pipeline-templates/README.md)
- [CRD templates](assets/crd-templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON/YAML configuration snippets, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-confirmed scope, explicit approval gates for writes, and least-privilege operational guidance.]

## Skill Version(s):

0.0.2 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
