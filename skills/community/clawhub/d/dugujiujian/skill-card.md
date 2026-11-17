## Description: <br>
独孤九剑V2 analyzes A-share stock codes by fetching public market data, computing technical features, matching a nine-swords rule system, and producing short-term market analysis with optional charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhc2026](https://clawhub.ai/user/yhc2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request A-share short-term technical analysis for a stock code, including rule matches, core indicators, support and resistance, and optional K-line chart generation. The output should be treated as analysis support rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party market-data providers using the stock codes a user asks about. <br>
Mitigation: Review applicable provider terms and run the skill only in environments where these outbound requests are acceptable. <br>
Risk: Market analysis can be incomplete, stale, or wrong if upstream data is delayed, unavailable, or misinterpreted. <br>
Mitigation: Treat outputs as analysis support, verify important signals independently, and avoid relying on the skill as financial advice. <br>
Risk: Chart generation writes PNG files locally. <br>
Mitigation: Run the skill in a workspace where local chart artifacts are expected and review generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhc2026/skills/dugujiujian) <br>
- [Nine-swords framework](artifact/knowledge/framework.md) <br>
- [MCP platform configuration guide](artifact/mcp_server/PLATFORM_CONFIGS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis report with JSON tool results and optional PNG chart paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact third-party market-data providers and write generated chart PNGs locally when charting is requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: artifact/SKILL.md frontmatter; ClawHub release: 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
