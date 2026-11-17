## Description:

A Chinese-language financial analysis toolkit that helps agents fetch and analyze public market data using OpenClaw tools, AKShare, pywencai, and web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to guide stock, industry, macroeconomic, and market-overview analysis from public data sources. It is intended to produce structured informational financial reports, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial analysis may contain stale, incomplete, or misleading market data.

Mitigation: Treat outputs as informational and verify source data before making financial decisions.

Risk: The skill may query AKShare, pywencai, and web search for public market data.

Mitigation: Install only when those data-source behaviors are expected for the deployment.

## Reference(s):

- [Financial Analysis Toolkit on ClawHub](https://clawhub.ai/paudyyin/skills/financial-analysis-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with optional Python code and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on public market data from AKShare, pywencai, and web search; users should verify data before financial decisions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
