## Description:

Fund Analysis helps agents analyze private and public funds using fof99 data, including NAV trends, performance metrics, holdings, screening, FOF portfolio analysis, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simpleeelv](https://clawhub.ai/user/simpleeelv)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, investors, and developers use this skill to retrieve fund data, compare fund performance, examine holdings, screen candidates, analyze FOF portfolios, and produce structured informational reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund names, fund codes, portfolio identifiers, and analysis parameters may be queried through the fof99 MCP data platform.

Mitigation: Confirm the user is comfortable sharing those identifiers before retrieval and avoid submitting sensitive portfolio details unless needed for the requested analysis.

Risk: Generated fund analysis may be mistaken for investment advice.

Mitigation: Present outputs as informational analysis, cite data sources and update dates, and avoid buy, sell, or hold recommendations unless a qualified reviewer provides them.

Risk: Chinese market conventions such as red for gains and green for losses may be unexpected for some audiences.

Mitigation: Ask for locale or color-format changes when the user expects different market presentation conventions.

## Reference(s):

- [Server-resolved GitHub source: simpleeelv/FOF99-SKILLS skills/Fund-Analysis](https://github.com/simpleeelv/FOF99-SKILLS/tree/main/skills/Fund-Analysis)
- [ClawHub skill page: Fund Analysis](https://clawhub.ai/simpleeelv/skills/fund-analysis-fof99)
- [ClawHub publisher profile: simpleeelv](https://clawhub.ai/user/simpleeelv)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reports with tables, concise analysis, and ECharts JSON chart configurations when visualization is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite data sources and update dates, include caveats for incomplete data, and avoid presenting analysis as investment advice.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
