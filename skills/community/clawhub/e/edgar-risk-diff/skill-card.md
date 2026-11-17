## Description:

Diffs the SEC 10-K Risk Factors section (Item 1A) between two filings for a US-listed ticker, surfacing added, removed, and modified risks, theme rollups, churn, and optional novelty scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hootriot08](https://clawhub.ai/user/hootriot08)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, investors, students, and developers use this skill to compare yearly 10-K Item 1A risk language, scan watchlists, and inspect changes in themes such as AI, cyber, geopolitics, regulation, and supply chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound SEC GET requests and sends an EDGAR User-Agent/contact string to sec.gov.

Mitigation: Install only when that network behavior is acceptable and set EDGAR_USER_AGENT to an appropriate contact string when redistributing.

Risk: Cached filings and an optional license key are stored under ~/.edgar-risk-diff/.

Mitigation: Do not put unrelated secrets in EDGAR_RISK_LICENSE or the license file; review or remove the local cache as needed.

Risk: Premium license gating is weak/placeholder-quality.

Mitigation: Treat the novelty subcommand license check as convenience gating, not strong access control.

Risk: Risk-factor extraction is regex-based and can miss non-standard 10-K HTML.

Mitigation: Use the latest command to inspect parsed Item 1A text and verify important results against the source filing before relying on them.

Risk: Output is informational and not legal or investment advice.

Mitigation: Have a qualified reviewer validate material conclusions before using the output in legal, investment, or compliance decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hootriot08/skills/edgar-risk-diff)
- [SEC EDGAR company tickers data](https://www.sec.gov/files/company_tickers.json)
- [SEC EDGAR submissions API](https://data.sec.gov/submissions/)
- [SEC EDGAR Archives](https://www.sec.gov/Archives/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports and tables with risk-factor excerpts, theme tags, churn metrics, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads public SEC EDGAR data, caches filings under ~/.edgar-risk-diff/, and optionally uses EDGAR_RISK_LICENSE or ~/.edgar-risk-diff/license.txt for premium novelty scoring.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
