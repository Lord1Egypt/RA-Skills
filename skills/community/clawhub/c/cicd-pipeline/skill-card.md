## Description:

Create, debug, and manage CI/CD pipelines with GitHub Actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, troubleshoot, and refine GitHub Actions workflows for testing, deployment, releases, publishing, secrets management, caching, and matrix builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows may deploy, publish, delete secrets, grant broad write permissions, or open debugging access if applied without review.

Mitigation: Review generated workflow changes before use, test deployment and publishing paths in staging first, restrict token permissions, and protect production environments with required reviewers.

Risk: Unpinned third-party actions or Docker images can introduce supply-chain drift.

Mitigation: Pin third-party actions and Docker images to immutable SHAs or digests, and review updates deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/cicd-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub Actions workflow snippets, GitHub CLI commands, deployment examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
