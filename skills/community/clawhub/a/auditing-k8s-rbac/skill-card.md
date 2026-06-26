## Description: <br>
Audits Kubernetes RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous bindings, service account exposure, and privilege escalation paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ling-qian](https://clawhub.ai/user/ling-qian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers and platform teams use this skill to audit Kubernetes RBAC in EKS, GKE, AKS, or self-managed clusters before remediation, access reviews, or compliance assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may require sensitive cluster-wide visibility into RBAC resources, service accounts, pods, and audit logs. <br>
Mitigation: Run it only with authorization and prefer a short-lived, dedicated read-only kubeconfig scoped to the resources needed for the audit. <br>
Risk: Generated reports can reveal cluster permissions, privileged workloads, service account usage, and other security posture details. <br>
Mitigation: Store and share audit outputs as sensitive security artifacts according to the organization's access-control and retention policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ling-qian/auditing-k8s-rbac) <br>
- [API Reference: Auditing Kubernetes Cluster RBAC](references/api-reference.md) <br>
- [Kubernetes RBAC documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) <br>
- [Kubernetes Python client](https://pypi.org/project/kubernetes/) <br>
- [KubiScan](https://github.com/cyberark/KubiScan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local RBAC audit reports such as k8s_rbac_audit.json; reports can contain sensitive cluster permissions and workload security posture.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
