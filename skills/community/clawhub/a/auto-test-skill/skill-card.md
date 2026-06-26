## Description: <br>
Analyzes stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlist alerts, dividend analysis, stock scoring, hot trend scanning, and rumor detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylfy-ljl](https://clawhub.ai/user/ylfy-ljl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and cryptocurrency analysis, track portfolios and watchlists, inspect dividend metrics, and surface market trends or early rumor signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional X/Twitter social scanning can require AUTH_TOKEN and CT0 values that function like account session credentials. <br>
Mitigation: Leave the X/Twitter feature disabled unless needed; if used, prefer a low-risk account, protect or delete the .env file, and verify the bird CLI source before use. <br>
Risk: The skill makes external market, news, and social requests and may produce incomplete, delayed, or misleading finance signals. <br>
Mitigation: Treat analysis as informational, verify important signals against primary sources, and consult a licensed financial advisor before making investment decisions. <br>
Risk: Portfolio and watchlist workflows store local user financial tracking data. <br>
Mitigation: Run with limited filesystem access where possible and review or remove local portfolio and watchlist files when they are no longer needed. <br>
Risk: Suggested cron automation can keep market scans running after the user no longer needs them. <br>
Mitigation: Review scheduled jobs periodically and remove any cron job when the monitoring workflow is no longer active. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ylfy-ljl/auto-test-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/ylfy-ljl) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner Documentation](docs/HOT_SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text analysis reports with shell command examples; some scripts support JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local portfolio and watchlist JSON files and may use optional environment credentials for X/Twitter social signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
