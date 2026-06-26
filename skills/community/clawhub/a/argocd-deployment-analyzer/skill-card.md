## Description: <br>
Analyze ArgoCD application sync status, detect configuration drift, review manifests for security and best practices, and diagnose sync failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to analyze ArgoCD-managed Kubernetes applications, investigate sync drift or failed syncs, and produce prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose ArgoCD and Kubernetes deployment details available to the user's current credentials. <br>
Mitigation: Use read-only, least-privilege credentials, verify the active kube context and ARGOCD_TOKEN, and begin with a specific application or project scope. <br>
Risk: All-application analysis can broaden the amount of cluster and deployment information inspected by the agent. <br>
Mitigation: Start with a named ArgoCD application or project before using the all-applications scope. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with command examples and YAML remediation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured findings include dashboard summary, drift report, failure diagnosis, health issues, configuration findings, security findings, ignoreDifferences recommendations, and prioritized action items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
