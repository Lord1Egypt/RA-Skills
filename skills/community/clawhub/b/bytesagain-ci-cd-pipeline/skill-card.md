## Description: <br>
Generate CI/CD pipeline configs for GitHub Actions, GitLab CI, and Jenkins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate starter CI/CD workflows, pre-deployment checklists, and rollback guidance for Node.js, Python, Go, Docker, Kubernetes, GitHub Actions, GitLab CI, and Jenkins projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI/CD examples may include deployment steps, secret references, branch triggers, and publish workflows that are unsafe if copied into a repository without review. <br>
Mitigation: Review generated workflows before use, restrict CI secrets to least privilege, add protected environments or manual approvals for production, and confirm branch and tag triggers match the intended release process. <br>
Risk: Generated deployment snippets contain placeholders for project-specific commands, infrastructure names, registries, and rollback operations. <br>
Mitigation: Replace placeholders with reviewed project values and test generated workflows in a non-production environment before enabling production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/bytesagain-ci-cd-pipeline) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and plain text containing CI/CD YAML, Jenkinsfile snippets, shell commands, deployment checklists, and rollback steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated examples include placeholders for deployment scripts, secrets, registries, Kubernetes resources, and project-specific commands that must be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
