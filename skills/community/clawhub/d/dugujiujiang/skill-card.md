## Description: <br>
Analyzes A-share stock tickers with a Nine Swords short-term trading framework by fetching market data, computing technical features, matching rule-based signals, and producing a concise trading-risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhc2026](https://clawhub.ai/user/yhc2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Chinese A-share tickers with automated data fetching, technical-feature calculation, rule matching, optional chart generation, and MCP tools. The output should be treated as market-analysis support, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external Chinese market-data or news providers for requested tickers. <br>
Mitigation: Install only where that network access is acceptable, preferably in a virtual environment with reviewed dependencies. <br>
Risk: Generated trading analysis may be mistaken for financial advice. <br>
Mitigation: Treat outputs as decision support and review market data, assumptions, and risk controls before taking action. <br>
Risk: Chart generation may create local PNG files. <br>
Mitigation: Run in a workspace where generated files are expected and remove chart artifacts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhc2026/skills/dugujiujiang) <br>
- [Nine Swords framework](knowledge/framework.md) <br>
- [MCP platform configurations](mcp_server/PLATFORM_CONFIGS.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown reports, JSON tool responses, and optional PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ticker-driven A-share analysis; may contact external market-data or news providers and save chart PNGs locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter: 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
