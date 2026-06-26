## Description: <br>
A Stock Monitor provides an A-share market monitoring workflow with market sentiment scoring, short- and long-term stock selection strategies, real-time price monitoring, leaderboards, a Flask web interface, scheduled data updates, and local historical data caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuchl2002](https://clawhub.ai/user/xuchl2002) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and technically capable investors can use this skill to run an A-share stock monitoring and screening assistant that collects market data, computes sentiment and technical indicators, and exposes results through commands, reports, and a local web dashboard. It is useful for research, monitoring, and decision-support workflows, not as a substitute for financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web app includes default credentials, a placeholder Flask secret key, debug mode, and a broad network bind. <br>
Mitigation: Before running the web app, replace default passwords, configure a real secret key, disable debug mode, and bind the service to localhost unless it is intentionally exposed behind appropriate network controls. <br>
Risk: Cron jobs and example webhook commands can run scripts repeatedly and send data outside the local environment. <br>
Mitigation: Review every scheduled command and webhook URL before enabling automation, and restrict schedules, payloads, and destinations to the intended environment. <br>
Risk: The skill writes cache, report, and application data under the skill directory. <br>
Mitigation: Run it in a workspace where those files are expected, review generated files periodically, and back up or clean local data according to the user's retention needs. <br>
Risk: Stock recommendations and sentiment scores can be incomplete, delayed, or wrong because they depend on third-party market data sources and technical indicators. <br>
Mitigation: Treat outputs as decision support only, validate material decisions against authoritative market data, and avoid using generated selections as financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuchl2002/a-stock-monitor-1-1-2) <br>
- [Publisher Profile](https://clawhub.ai/user/xuchl2002) <br>
- [API Reference](references/API.md) <br>
- [Installation Guide](references/INSTALL.md) <br>
- [Stock Selection Guide](references/STOCK_SELECTION.md) <br>
- [Data Source Summary](references/DATA_SOURCE_FINAL.md) <br>
- [Sina Test Report](references/SINA_TEST_REPORT.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Changelog](references/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON API responses, configuration values, and generated report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite cache files, stock-selection report files, cron schedules, and a local Flask web service when the user runs the included scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata and changelog document upstream app version 1.1.2, released 2026-02-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
