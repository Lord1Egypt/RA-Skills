## Description:

Automates CI/CD pipelines for GitHub Actions, GitLab CI, and Jenkins with build, test, deploy workflow creation and pipeline status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to create GitHub Actions workflows and GitLab CI configurations, monitor CI pipeline status, and reason about deployment automation across common CI/CD platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI/CD files or deployment automation could affect production systems if applied without review.

Mitigation: Inspect generated workflow and pipeline files before committing them, and require normal code review and environment approval for deployment changes.

Risk: Pipeline monitoring can involve GitHub, GitLab, or Jenkins credentials.

Mitigation: Use narrowly scoped, short-lived tokens stored in secret managers or environment variables, and avoid passing tokens directly on command lines.

Risk: Untrusted or plaintext GitLab URLs can expose tokens or pipeline data.

Mitigation: Use trusted HTTPS GitLab endpoints and validate URLs before calling pipeline APIs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/ci-cd-pipeline-toolkit)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline code, YAML configuration examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated CI/CD configuration and deployment guidance should be reviewed before being committed or applied to production systems.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
