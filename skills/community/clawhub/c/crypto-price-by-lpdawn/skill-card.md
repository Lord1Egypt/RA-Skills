## Description:

Looks up real-time USD prices for major cryptocurrencies such as BTC and ETH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpdawn](https://clawhub.ai/user/lpdawn)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer current cryptocurrency price questions by querying Binance through ccxt and returning a short price and 24-hour change response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Binance for live market prices.

Mitigation: Use it only in environments where outbound requests to Binance are acceptable.

Risk: The skill depends on the local Python environment having ccxt available.

Mitigation: Confirm ccxt is installed before relying on the skill.

Risk: Unsupported symbols or exchange availability issues can cause lookup failures.

Mitigation: Ask the user to confirm the symbol or retry later when the exchange is unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lpdawn/skills/crypto-price-by-lpdawn)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text price response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to BTC when no symbol is provided; reports query failures as plain text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
