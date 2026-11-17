## Description:

Optimize CI/CD build caching across GitHub Actions, GitLab CI, CircleCI, and Jenkins — analyze cache hit rates, recommend cache keys, and reduce build times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to analyze CI/CD cache configuration, identify cache misses or weak cache keys, and produce platform-specific recommendations that can reduce build time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cache configuration may be incorrect or inefficient for a specific repository or CI platform.

Mitigation: Review generated cache keys, paths, restore keys, and platform-specific settings before applying them.

Risk: The skill may inspect or reason about CI configuration files when asked about caching or build time.

Mitigation: Limit shared inputs to the CI files needed for cache analysis and avoid including secrets or unrelated repository data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline YAML or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes actionable CI cache recommendations, projected build-time improvements, and reviewable configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
