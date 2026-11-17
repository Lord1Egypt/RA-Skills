## Description:

Audits Kubernetes RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous ClusterRoleBindings, service account abuse, and privilege escalation paths using kubectl, rbac-tool, KubiScan, and Kubeaudit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ling-qian](https://clawhub.ai/user/ling-qian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and security teams use this skill to audit Kubernetes cluster RBAC policies, bindings, and service accounts for least-privilege gaps and privilege escalation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be run with cluster-admin or equivalent credentials for a read-oriented audit.

Mitigation: Use a dedicated, short-lived, read-only Kubernetes audit identity instead of production cluster-admin credentials.

Risk: The workflow relies on third-party audit tools that may be installed without pinned versions.

Mitigation: Pin and verify rbac-tool, KubiScan, Kubeaudit, and related dependencies before use.

Risk: Generated RBAC reports can expose sensitive cluster structure, subjects, bindings, and permissions.

Mitigation: Store reports only in approved locations with access controls appropriate for security audit data.

## Reference(s):

- [API Reference: Auditing Kubernetes Cluster RBAC](references/api-reference.md)
- [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes Python client](https://pypi.org/project/kubernetes/)
- [KubiScan](https://github.com/cyberark/KubiScan)
- [ClawHub skill page](https://clawhub.ai/ling-qian/skills/auditing-k8s-rbac)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and optional JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Kubernetes RBAC findings, remediation notes, and local report files such as k8s_rbac_audit.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
