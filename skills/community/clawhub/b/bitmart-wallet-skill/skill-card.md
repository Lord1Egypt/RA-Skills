## Description:

BitMart Web3 Wallet Skills provides agent guidance for 12 public BitMart Web3 API endpoints covering token search, chain details, token info, K-line charts, rankings, smart money analysis, address balances, recent transactions, swap quotes, and batch prices without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mccoysc](https://clawhub.ai/user/mccoysc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to look up BitMart Web3 token, market, smart money, wallet balance, recent transaction, and quote data across Solana, BSC, Ethereum, Arbitrum, and Base. It helps agents resolve token identifiers, select compatible chains, and prepare BitMart public API requests for read-only analysis and swap quote workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet address lookups can expose privacy-sensitive public on-chain activity to BitMart API endpoints.

Mitigation: Submit wallet addresses only when there is a legitimate reason to inspect that public activity, and avoid addresses that identify a person unless necessary.

Risk: Market, ranking, smart money, and swap quote results may be incomplete, rate-limited, or unavailable for a requested token pair or chain.

Mitigation: Resolve token and chain identifiers through the documented workflow, confirm same-chain swap compatibility, and retry later when BitMart returns rate-limit errors.

## Reference(s):

- [BitMart homepage](https://www.bitmart.com)
- [BitMart Web3 API base URL](https://api-cloud.bitmart.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; BitMart documents a limit of 15 requests per second per IP.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
