## Description:

Caching strategies, invalidation, eviction policies, HTTP caching, distributed caching, and anti-patterns. Use when designing cache layers, choosing eviction policies, debugging stale data, or optimizing read-heavy workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design cache layers, choose caching and eviction strategies, configure HTTP caching behavior, debug stale data, and optimize read-heavy systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends an unpinned remote npx install path for a Markdown-only skill, which can give installer code broad local access.

Mitigation: Review the installation path before installing, prefer a pinned and verified source or manual copy of reviewed files, and avoid running the npx install command with elevated privileges.

Risk: Caching guidance can lead to stale data, sensitive data exposure, or unreliable systems if applied without application-specific review.

Mitigation: Review proposed cache strategies against the source-of-truth model, data sensitivity, invalidation requirements, TTL policy, and monitoring expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/caching)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with tables and inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cache strategy comparisons, HTTP Cache-Control examples, Redis or Memcached guidance, invalidation recommendations, monitoring advice, and anti-pattern warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
