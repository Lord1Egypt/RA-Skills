## Description:

Fetch optimal swap quotes from the OKX DEX Aggregator API v6 and generate authenticated quote calls with token amount formatting, routing details, price-impact checks, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronllee](https://clawhub.ai/user/aaronllee)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to query real-time DEX aggregator pricing, compare swap routes, and generate code or commands for quote-only OKX Web3 API integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires OKX Web3 API credentials and sends quote parameters to OKX.

Mitigation: Use environment variables or a trusted secrets manager, avoid logging credentials or signatures, and install only when sharing quote details with OKX is acceptable.

Risk: Precision-sensitive trades can be affected by human-readable amount conversion and Python float handling.

Mitigation: Pass raw token amounts when possible, verify token decimals, and review or adjust amount conversion before relying on results for financial decisions.

Risk: Dependency installation can introduce supply-chain exposure.

Mitigation: Install dependencies such as requests from trusted package sources and review the environment before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronllee/skills/dex-quote)
- [OKX DEX Aggregator quote endpoint](https://web3.okx.com/api/v6/dex/aggregator/quote)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets, CLI examples, and quote summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, environment-variable setup guidance, parsed quote summaries, route details, price-impact warnings, and honeypot or token-tax warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
