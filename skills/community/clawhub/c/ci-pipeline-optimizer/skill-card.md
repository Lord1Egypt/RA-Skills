## Description:

Analyze CI/CD pipelines (GitHub Actions, GitLab CI, CircleCI) and suggest optimizations - caching strategies, parallelization, step elimination, Docker layer optimization, matrix builds, and conditional execution to reduce build times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to statically review CI/CD configuration files and Dockerfiles for opportunities to reduce build time and CI cost. It supports pipeline maintenance tasks such as cache recommendations, parallelization review, path filtering, Docker build optimization, and optimized workflow suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI configuration may introduce incorrect workflow behavior or unexpected build cost changes if applied without review.

Mitigation: Review generated YAML and recommendations before applying them to a repository.

Risk: The skill may inspect CI workflow files and Dockerfiles in the repository.

Mitigation: Run it only against repositories whose CI configuration you are prepared to share with the agent.

Risk: Log-based analysis may expose CI logs even though the release evidence notes a documentation inconsistency around log access.

Mitigation: Avoid providing CI logs unless log-based analysis is explicitly intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable analysis, JSON summaries, Markdown reports, and YAML workflow configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static analysis only; recommendations and generated CI configuration should be reviewed before applying.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
