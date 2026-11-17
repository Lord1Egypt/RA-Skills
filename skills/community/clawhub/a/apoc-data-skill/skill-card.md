## Description:

Use when users ask for A-share stock quotes, financials, capital flows, technical factors, announcements, sectors, convertible bonds, macro data, or comprehensive stock analysis through the ApocData public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjialegit](https://clawhub.ai/user/hanjialegit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents query ApocData's read-only public A-share market data endpoints and produce research-oriented market, company, sector, convertible bond, and macro analysis. Outputs must remain research assistance and not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions use unverified remote downloads that write into an auto-loaded agent skill directory.

Mitigation: Prefer a manually downloaded, pinned, checksum- or signature-verified release before installation; avoid curl-to-shell and remote archive streaming unless the publisher and release contents are trusted.

Risk: Financial analysis may be misleading if delayed, stale, sparse, or failed API responses are treated as current or complete.

Mitigation: Check HTTP status, success fields, freshness headers, trade dates, delay fields, and sparse-data signals before drawing conclusions; present outputs as research assistance, not investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanjialegit/skills/apoc-data-skill)
- [ApocData Platform](https://www.apocdata.com)
- [ApocData OpenAPI Specification](https://www.apocdata.com/api/blade-dataplatform/open/data/openapi.json)
- [Interface Boundaries](references/boundaries.md)
- [Financial Output Safety Rules](references/safety-rules.md)
- [Usage Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite data freshness, distinguish raw API data from model inference, and include a financial research disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
