## Description:

Guides agents through rigorous high-stakes decision analysis for investments, major purchases, technology selection, supplier choice, and other hard-to-reverse commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make high-stakes decisions with explicit constraints, current data checks, comparison matrices, transparent methodology, exit conditions, and follow-up tracking. It is especially suited to investment, purchase, vendor, and technology-selection workflows where stale data or unsupported conclusions would create financial or operational risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision guidance may rely on stale or unavailable market, product, or vendor data.

Mitigation: Verify current prices, dates, and assumptions independently before spending money, signing contracts, or opening positions.

Risk: The included audit script can miss context-specific financial or operational issues.

Mitigation: Use the script as a checklist aid and require human review for methodology, data freshness, assumptions, and downside cases.

## Reference(s):

- [Decision Workflow](references/decision-workflow.md)
- [Investment Playbook Template](references/investment-playbook-template.md)
- [Decision Audit Script](references/audit-script-decision.sh)
- [Skill Page](https://clawhub.ai/christianye/skills/build-protocol-decision)
- [Stooq Market Data CSV](https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv)
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart/SYMBOL)
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown with decision matrices, rationale, risk controls, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current-data verification steps, stop-loss or exit conditions, position sizing, daily P/L tracking guidance, and audit findings.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
