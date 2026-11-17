## Description:

Generates CI/CD workflow files for GitHub Actions, GitLab CI, and Jenkins based on a project's language, framework, testing, deployment, and release options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small teams use this skill to generate CI/CD workflow configuration for Python, JavaScript, and Go projects, including tests, Docker builds, cloud deployment steps, and release jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some generated templates can pipe remote scripts into bash for Codecov or GoReleaser.

Mitigation: Review or replace those steps with pinned, verified actions or locally managed tooling before committing the workflow.

Risk: Generated deploy and publish jobs can use cloud, registry, package, or repository credentials.

Mitigation: Enable only the jobs that are required, scope CI secrets tightly, and restrict credentialed jobs to protected branches, tags, environments, and isolated runners.

Risk: The generated workflow may not match a project's dependency, deployment, or release controls without adjustment.

Mitigation: Review every generated workflow, verify deploy and publish behavior, and test it in a non-production CI environment before enabling it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/shenghoo123-png/skills/cicd-templates-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and generated CI/CD configuration files, including YAML workflows and Jenkinsfile text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content may be printed to stdout or written as ci.yml, .gitlab-ci.yml, Jenkinsfile, or all supported formats.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
