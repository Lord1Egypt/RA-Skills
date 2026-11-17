## Description:

Generate CI/CD pipeline configs for GitHub Actions, GitLab CI, and Jenkins for Node.js, Python, Go, Docker, and Kubernetes projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to generate starter CI/CD workflows, deployment checklists, and rollback guidance when setting up or reviewing release automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment templates can handle production credentials and deployment permissions.

Mitigation: Review and harden generated workflows before installing them; use least-privilege tokens and Kubernetes RBAC, job-scoped temporary kubeconfig files with mode 0600, and production branch or environment approvals.

Risk: Generated workflows may include mutable third-party CI dependencies.

Mitigation: Pin third-party actions and reusable CI dependencies to reviewed commit SHAs before production use.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-ci-cd-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, Jenkinsfile, shell command, checklist, and rollback strategy content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated templates vary by CI platform and stack and should be reviewed before installation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
