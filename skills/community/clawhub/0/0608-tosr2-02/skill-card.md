## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlists, alerts, dividend analysis, stock scoring, trend detection, and rumor or early-signal scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run market-analysis workflows for equities and cryptocurrencies, manage portfolios and watchlists, and surface trending or rumor-driven market signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twitter/X integration may expose sensitive X session credentials to the skill and the bird CLI. <br>
Mitigation: Prefer running hot scans with --no-social unless social data is required; if enabled, use a dedicated low-privilege account and keep AUTH_TOKEN and CT0 out of version control. <br>
Risk: Broad environment secrets may be forwarded to an external CLI. <br>
Mitigation: Keep unrelated secrets out of the skill .env and review the environment before running commands that enable social-data collection. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/0608-tosr2-02) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local portfolio and watchlist JSON files under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter declares 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
