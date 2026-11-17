## Description:

AI-powered Chinese A-share stock analyst that fetches real-time market data, technical indicators, valuations, and news via AkShare, then generates scored investment analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chienchandler](https://clawhub.ai/user/chienchandler)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Chinese A-share stocks, compare stocks, review market or sector conditions, and generate informational scored analysis reports. It is intended for research support, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock scores and reports may be mistaken for investment advice.

Mitigation: Present outputs as informational research only, include the disclaimer, and require users to do their own review before making investment decisions.

Risk: The skill contacts AkShare-backed sources, Sina Finance, EastMoney, and Xueqiu, and news content may be incomplete or manipulated.

Mitigation: Tell users which data sources were used, call out missing data, and avoid treating news-driven signals as definitive.

Risk: The AkShare dependency is not pinned to an exact version.

Mitigation: Install and run the skill in an isolated Python environment and review dependency changes before operational use.

## Reference(s):

- [AI Stock Analyst on ClawHub](https://clawhub.ai/chienchandler/skills/ai-stock-analyst)
- [Project homepage](https://github.com/chienchandler/ai-stock-analyst)
- [A-Share Stock Analysis Guide](references/analysis-guide.md)
- [Prompt Templates for Stock Analysis](references/prompt-templates.md)
- [AkShare](https://github.com/akfamily/akshare)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis report with supporting JSON from local data-fetch scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a -5.00 to +5.00 score, key findings, technical analysis, fundamental analysis, news and sentiment, conclusion, and disclaimer.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
