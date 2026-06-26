## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists with alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stock, crypto, portfolio, watchlist, dividend, hot-market, and rumor-signal analyses from market and news data. It is intended for informational finance workflows and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional social scanning can use live Twitter/X session credentials through AUTH_TOKEN and CT0. <br>
Mitigation: Prefer finance scans without social data or use --no-social; if social scanning is required, keep credentials out of git and logs, restrict file permissions, and rotate or revoke exposed tokens. <br>
Risk: The Twitter/X workflow can require trusting the bird CLI and may request broad local browser access. <br>
Mitigation: Do not grant Terminal Full Disk Access or browser-cookie access unless the operator explicitly accepts that workflow; use the least-privileged token setup available. <br>
Risk: Finance outputs may be stale, incomplete, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as informational analysis, review source data freshness and caveats, and require qualified human review before trading or investment use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0605-tosr2-cisg-02) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [bird CLI](https://github.com/steipete/bird) <br>
- [Usage guide](docs/USAGE.md) <br>
- [Hot Scanner documentation](docs/HOT_SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain-text and Markdown-style terminal reports with optional JSON output and inline bash commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market recommendations, confidence scores, caveats, portfolio summaries, alert checks, trend rankings, and local configuration guidance.] <br>

## Skill Version(s): <br>
6.2.0 (source: artifact/SKILL.md frontmatter); ClawHub release 1.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
