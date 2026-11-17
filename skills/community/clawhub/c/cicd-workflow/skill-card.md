## Description:

Provides CI/CD workflow templates and setup guidance for Java and Vue projects using GitLab CI or Jenkins, with linting, testing, builds, Docker image creation, Kubernetes deployment, and deployment notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallest-ming](https://clawhub.ai/user/smallest-ming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to generate CI/CD pipeline files, setup guides, and deployment configuration for Java, Vue, or full-stack Java plus Vue projects. It is intended for teams configuring GitLab CI or Jenkins workflows with Docker, Kubernetes, SSH deployment, quality checks, testing, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production CI/CD guidance can grant root-equivalent access when Docker TCP exposure, host docker.sock mounts, privileged runners, or sudo-enabled deployment users are followed without hardening.

Mitigation: Treat generated pipelines as starting templates; remove Docker TCP exposure, avoid host docker.sock and privileged runners for general jobs, and keep deployment users out of broad sudo groups.

Risk: Deployment credentials and kubeconfig material can provide broad cluster or registry access if stored or used without sufficient controls.

Mitigation: Use secure CI secret mechanisms, rotate credentials, scope Kubernetes service accounts to least privilege, and require approvals for production deployments.

Risk: Use of floating image tags such as latest can make production deployments non-reproducible and harder to audit.

Mitigation: Pin base images and deployment images to explicit versions or immutable digests, and promote tested artifacts through controlled environments.

Risk: Generated project names and paths may be inserted into shell commands or service files.

Mitigation: Validate project names against a conservative allowlist and quote shell variables before using generated commands in CI jobs or deployment scripts.

## Reference(s):

- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab Runner Installation](https://docs.gitlab.com/runner/install/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Kubernetes Deployment Guide](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with CI/CD configuration snippets, pipeline files, shell commands, and generated setup guides.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable templates for GitLab CI, Jenkins, Docker, Kubernetes, Nginx, notification webhooks, and setup documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
