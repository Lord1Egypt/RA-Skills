## Description:

Analyze ArgoCD application sync status, detect configuration drift, review manifests for security and best practices, and diagnose sync failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to investigate ArgoCD-managed applications, diagnose sync failures and drift, audit deployment configuration, and produce prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Over-broad ArgoCD or Kubernetes access could inspect more applications, namespaces, or clusters than intended.

Mitigation: Use read-only permissions scoped to the requested application or project, and avoid all-cluster scans unless that scope is intentional.

Risk: Manifest exports can include sensitive deployment details, and fixed temporary paths may leave data behind.

Mitigation: Use secure temporary files with restrictive permissions and clean them up after analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/argocd-deployment-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dashboard summaries, drift analysis, failure diagnosis, health findings, security findings, and prioritized action items.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
