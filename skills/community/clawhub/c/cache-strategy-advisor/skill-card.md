## Description:

Design and optimize caching strategies for applications. Analyze data access patterns, recommend cache layers (browser, CDN, application, database), configure TTLs, invalidation policies, and measure cache hit rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess cache layers, measure cache hit rates, diagnose stale data or low hit-rate issues, and produce cache strategy recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic commands can inspect local cache statistics, search project code, and contact the configured host for cache headers.

Mitigation: Review commands and target hosts before running diagnostics against production systems.

Risk: Cache configuration guidance can introduce stale data, low hit rates, or excessive cache pressure if applied without validation.

Mitigation: Validate TTLs, invalidation rules, and hit-rate measurements in the target environment before production rollout.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cache strategy reports, cache policy recommendations, diagnostic commands, and implementation snippets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
