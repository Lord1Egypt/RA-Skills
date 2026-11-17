## Description:

Generate GitHub Actions CI/CD pipelines tailored to the current project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a repository, identify its stack, and generate GitHub Actions CI, Docker, and deployment workflows tailored to the project's scripts and deployment target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment workflows may use sensitive deployment credentials.

Mitigation: Review each generated secret reference, scope tokens narrowly, and protect production environments with required reviewers before committing workflows.

Risk: Some deployment templates use mutable or unpinned third-party tooling.

Mitigation: Pin third-party actions to reviewed commit SHAs and pin deployment CLI versions or use locked project dependencies.

Risk: VPS deployment examples may restart services with privileged commands.

Mitigation: Avoid unrestricted sudo for deploy users and limit restart permissions to the specific service required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llcsamih/skills/cicd-generator)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML workflow files and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create GitHub Actions workflow files and provide deployment secret checklists when used by an agent.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
