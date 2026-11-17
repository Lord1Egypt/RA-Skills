## Description:

Agent Stock helps agents retrieve real-time stock market data for stock screening, trading decisions, holdings analysis, and quantitative trading decision workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anoyix](https://clawhub.ai/user/anoyix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen stocks, analyze individual symbols or current holdings, and produce short-term, risk-aware trading decision reports from real-time market data. Outputs should be treated as informational and independently verified before any trading action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install unpinned third-party Python package code.

Mitigation: Install only from a trusted package source and review the package before use.

Risk: Trading guidance may be incorrect, incomplete, or misleading.

Mitigation: Treat all outputs as informational and independently verify them before any trading action.

Risk: Holdings and trading reports may contain sensitive account or portfolio information.

Mitigation: Avoid providing brokerage credentials or unnecessary account details, and require explicit confirmation before saving reports locally.

## Reference(s):

- [Holdings analysis workflow](references/holdings.md)
- [Quantitative trading decision workflow](references/quant.md)
- [Quantitative scoring rules](references/quant_rule.md)
- [Stock screening workflow](references/screen.md)
- [Individual stock trading decision workflow](references/trade.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with tables, concise trading guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save screening, trading, quantitative, or holdings reports under dist/.]

## Skill Version(s):

0.2.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
