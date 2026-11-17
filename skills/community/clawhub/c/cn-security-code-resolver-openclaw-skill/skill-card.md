## Description:

Resolve A-share stocks, ETFs, funds, and other mainland China securities from Chinese names into tradable codes using Eastmoney search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-11even](https://clawhub.ai/user/mr-11even)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve Chinese security names into tradable mainland China stock, ETF, fund, or REIT codes and to enrich watchlists or portfolio files with exchange-aware identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security names or watchlist entries are sent to Eastmoney for lookup.

Mitigation: Review queries before running batch resolution and submit only the minimum names needed for sensitive portfolios.

Risk: Ambiguous Chinese security names can return multiple matching stocks, funds, or market listings.

Mitigation: Check exact name, security type, market metadata, and top candidates before writing resolved codes into user files.

## Reference(s):

- [Eastmoney Suggest API Reference](references/eastmoney-api.md)
- [Eastmoney suggest API endpoint](https://searchapi.eastmoney.com/api/suggest/get)
- [ClawHub skill page](https://clawhub.ai/mr-11even/skills/cn-security-code-resolver-openclaw-skill)
- [Publisher profile](https://clawhub.ai/user/mr-11even)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON resolver output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes raw numeric code, exchange suffix, standard code, security type, quote ID, and source metadata when resolution succeeds.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
