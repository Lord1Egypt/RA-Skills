## Description:

Provides sourced, time-stamped research on Hyperliquid markets, funding, liquidity, risks, and trading claims without placing trades or accessing a wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders, analysts, and developers use this skill to assess Hyperliquid markets or test trading claims against current public data before deciding whether further planning is warranted. It provides research, not financial advice, account monitoring, or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stale or incomplete market data can make a trading conclusion unreliable.

Mitigation: Verify live facts against current public sources, date each observation, and report unavailable evidence instead of making current claims.

Risk: Financial research may be mistaken for a trade recommendation or authorization.

Mitigation: Treat the output as research, assess the possibility of losing the full margin balance, and require a separate, explicitly requested workflow for any signer, fee approval, or execution action.

## Reference(s):

- [Hyperliquid Analysis on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-hyperliquid-analyze)
- [Hyperliquid documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/llms.txt)
- [Hyperliquid Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Research output contract](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research report with dated evidence, risk assessment, conditional verdict, and next evidence steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Names network and market identity, distinguishes observed facts from assumptions, and marks unavailable live data explicitly.]

## Skill Version(s):

0.4.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
