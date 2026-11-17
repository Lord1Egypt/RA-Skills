## Description:

Automate builds, tests, and deployments across web, mobile, and backend applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose CI/CD platforms, create workflow templates, improve build caching, configure mobile signing, and debug failing builds for web, mobile, backend, and monorepo projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable CI/CD workflow examples may be copied into repositories with unsafe deployment assumptions.

Mitigation: Review and harden workflows before installation, including minimal permissions, environment approvals, restricted deployment keys and sudo rights, and safe publication settings for Docker images or mobile artifacts.

Risk: Third-party actions and mutable dependencies in workflow examples can change behavior unexpectedly.

Mitigation: Pin third-party actions and runtime images to reviewed versions or commits before using the examples in production pipelines.

Risk: Secrets used by CI jobs can be exposed through pull-request workflows or deployment steps.

Mitigation: Keep secrets in platform secret stores, avoid exposing them to untrusted pull-request jobs, and prefer OIDC or scoped credentials where supported.

## Reference(s):

- [CI/CD Templates](templates.md)
- [Mobile CI/CD Patterns](mobile.md)
- [Web CI/CD Patterns](web.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copy-paste CI/CD workflow examples and troubleshooting guidance; examples require review before use in a repository.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
