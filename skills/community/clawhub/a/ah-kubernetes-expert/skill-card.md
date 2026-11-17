## Description:

Provides Kubernetes expertise for cluster architecture, workload orchestration, service mesh management, custom resource definitions, Helm charts, security, performance, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to draft, review, and troubleshoot Kubernetes manifests, Helm charts, RBAC policies, service and ingress configurations, monitoring setup, and operational runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Kubernetes manifests or examples could grant overly broad cluster access to secrets and workloads.

Mitigation: Review manifests before use and replace cluster-wide RBAC with namespace-scoped least-privilege roles.

Risk: Troubleshooting guidance could encourage listing or inspecting secrets without proper authorization.

Mitigation: Avoid listing or describing secrets unless explicitly authorized and operationally necessary.

Risk: Example infrastructure dependencies and observability endpoints could be deployed with weak defaults.

Mitigation: Enable Redis authentication, pin Helm dependencies, and expose monitoring endpoints only inside trusted observability environments.

## Reference(s):

- [Kubernetes Expert Code Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-kubernetes-expert)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, Go, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kubernetes manifests, Helm configuration, security configuration, monitoring setup, troubleshooting guides, and operational runbooks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
