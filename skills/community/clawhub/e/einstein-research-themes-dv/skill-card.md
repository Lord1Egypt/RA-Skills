## Description:

Detect and analyze trending market themes across sectors for current market themes, trending sectors, sector rotation, thematic investing, and bullish or bearish market narratives with lifecycle analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to detect, rank, and explain bullish and bearish market themes across sectors using momentum, volume, breadth, lifecycle, ETF, and narrative signals. It supports theme-level market analysis and thematic allocation research, not individualized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions can expose API keys if users run commands that print credential values.

Mitigation: Use presence checks instead of echoing secrets, avoid logging credentials, and rotate any key that may have been printed into logs.

Risk: Dependencies and outbound network access are under-hardened.

Mitigation: Run the skill in an isolated environment with pinned dependencies and expect outbound requests to FINVIZ, FMP, yfinance, GitHub data sources, and web search providers.

Risk: Generated theme reports may be mistaken for financial advice.

Mitigation: Treat outputs as informational market analysis and review results before making investment decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/clawdiri-ai/skills/einstein-research-themes-dv)
- [Cross-Sector Theme Definitions](references/cross_sector_themes.md)
- [Theme Detection Methodology](references/theme_detection_methodology.md)
- [Thematic ETF Catalog](references/thematic_etf_catalog.md)
- [FINVIZ Industry Codes](references/finviz_industry_codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural-language analysis with optional Markdown reports, JSON report files, Python commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are informational market analysis and may rely on FINVIZ, FMP, yfinance, GitHub-hosted data sources, and web search for narrative confirmation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; source skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
