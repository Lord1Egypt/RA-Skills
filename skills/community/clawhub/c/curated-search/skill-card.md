## Description:

Domain-restricted full-text search over curated technical documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qsmtco](https://clawhub.ai/user/qsmtco)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to query a local, domain-restricted index of curated technical documentation and retrieve authoritative results without general web search noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional crawling can make outbound HTTP requests and has network-safety gaps identified by the ClawHub security summary.

Mitigation: Keep the crawler disabled unless needed, review config.yaml domains and seeds before crawling, avoid untrusted domains, and run crawls in a network-restricted environment when possible.

Risk: Overly broad crawl configuration can expand collection beyond the intended curated documentation set.

Mitigation: Use trusted, specific documentation domains, keep robots.txt enabled, and keep crawl depth and concurrency conservative.

Risk: Node dependencies and local index files affect runtime trust for search results.

Mitigation: Update dependencies before production use and rebuild the index from reviewed configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qsmtco/skills/curated-search)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Domain Guide](DOMAIN_GUIDE.md)
- [Deployment and Operations Guide](docs/deployment.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON search results returned to the agent, often summarized as concise text with source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; search is local after an index is built, while optional index crawling follows config.yaml.]

## Skill Version(s):

1.0.7 (source: server release metadata, SKILL.md frontmatter, changelog released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
