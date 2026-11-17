## Description:

Operate DexScreener public market data APIs through UXC with a curated OpenAPI schema, no-auth setup, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to query DexScreener public market data for token profiles, boosts, pair searches, pair lookups, and token market rows without adding trading or wallet authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned DexScreener market data may be noisy or incomplete, especially for long-tail tokens.

Mitigation: Use the data for read-only lookup and analysis, verify important market observations against additional sources, and do not treat results as investment advice.

Risk: Polling discovery feeds can hit endpoint-specific DexScreener rate limits.

Mitigation: Prefer narrow reads, start with single-token or short address-list lookups, and cache results when polling profiles or boosts.

Risk: The skill relies on network access to DexScreener and the disclosed OpenAPI schema URL.

Mitigation: Confirm the agent is allowed to query https://api.dexscreener.com and fetch the schema URL before installation or execution.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/dexscreener-public.openapi.json)
- [DexScreener API reference](https://docs.dexscreener.com/api/reference)
- [Skill page](https://clawhub.ai/jolestar/skills/dexscreener-openapi-skill)
- [Publisher profile](https://clawhub.ai/user/jolestar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve the UXC JSON envelope and keep DexScreener activity read-only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
