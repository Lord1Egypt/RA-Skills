## Description: <br>
AI Stock Analyst helps agents fetch Chinese A-share market data, technical indicators, valuations, and news, then produce scored informational stock analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chienchandler](https://clawhub.ai/user/chienchandler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Chinese A-share stocks, compare multiple stocks, review market or sector context, and generate concise scored reports for informational research. The skill is not intended to provide investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analysis may be incomplete, stale, or misleading when market data, valuation data, or news sources are unavailable or delayed. <br>
Mitigation: Clearly state missing data, keep the informational-use disclaimer, and require human review before using outputs for financial decisions. <br>
Risk: The helper scripts contact external market and news services during use. <br>
Mitigation: Review requested network access and avoid providing credentials or write permissions unless they match the user's intent. <br>


## Reference(s): <br>
- [Analysis Guide](references/analysis-guide.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Skill homepage](https://github.com/chienchandler/ai-stock-analyst) <br>
- [AkShare](https://github.com/akfamily/akshare) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON data from helper scripts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a numeric score, findings, technical and fundamental analysis, news context, risk factors, and an informational-use disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
