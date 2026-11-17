## Description:

Scans meme coins for scam signals, rug-pull risk, on-chain audit flags, liquidity status, new listings, and trending-token context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect meme-token addresses, review new or trending token listings, and produce cautionary checklist guidance before making token decisions. Outputs are informational and should be verified with independent scanners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an undisclosed utility script unrelated to the advertised meme-coin scanner and evidence reports it can persist user-supplied arguments locally.

Mitigation: Review the package before installation, use only the advertised scanner workflow when appropriate, and do not pass secrets or sensitive values to the hash, encrypt, or password utility commands.

Risk: Scanner results and token listings can be incomplete, delayed, rate-limited, or misleading if used as the sole basis for a financial decision.

Mitigation: Verify findings with multiple independent scanners, contract explorers, liquidity-lock checks, and small test transactions before committing funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-meme-coin-scanner)
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog)
- [BytesAgain homepage](https://bytesagain.com)
- [DexScreener token API](https://api.dexscreener.com/latest/dex/tokens/{})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown-style guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner output may include externally fetched market data and manual follow-up links; outputs are not financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
