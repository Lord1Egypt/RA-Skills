## Description: <br>
You are a Kubernetes expert with deep knowledge of container orchestration, cluster management, and cloud-native architectures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to design Kubernetes manifests, Helm configurations, security controls, monitoring setups, troubleshooting steps, and operational runbooks for cloud-native workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Kubernetes manifests or commands can affect live cluster resources if applied without review. <br>
Mitigation: Review and adapt all manifests and commands for the target namespace, cluster policy, and operational context before applying them. <br>
Risk: Powerful RBAC examples and secret-inspection commands may expose sensitive data or grant broader access than needed. <br>
Mitigation: Prefer least-privilege Role and RoleBinding resources over cluster-wide grants, and avoid listing or describing Secrets unless there is a specific authorized operational need. <br>


## Reference(s): <br>
- [Kubernetes Expert Code Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, Go, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Kubernetes manifests, Helm chart snippets, security configuration, monitoring and alerting setup guidance, troubleshooting guides, and operational runbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
