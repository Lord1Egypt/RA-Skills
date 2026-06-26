## Description: <br>
ClawWatch helps agents manage crypto and stock watchlists, fetch prices, set alerts, export data, and check the Crypto Fear & Greed Index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goarstne](https://clawhub.ai/user/goarstne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use ClawWatch to maintain a market watchlist, fetch current crypto and stock prices, set alerts, and summarize machine-readable CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market prices and alerts can be stale, unavailable, or affected by third-party API rate limits. <br>
Mitigation: Summarize prices as current at fetch time, use the JSON output for clarity, and avoid running checks more often than the documented 60-second interval. <br>
Risk: Watchlist notes, cached files, exports, and analysis handoffs can reveal sensitive portfolio details. <br>
Mitigation: Avoid storing sensitive details in notes and share watchlist JSON with another agent only when the user intends that sharing. <br>
Risk: Optional market data API keys can be exposed if copied into prompts, logs, or exported files. <br>
Mitigation: Treat configured API keys as private configuration and do not include them in summaries, prompts, or exports. <br>


## Reference(s): <br>
- [ClawWatch ClawHub listing](https://clawhub.ai/goarstne/clawwatch) <br>
- [ClawWatch API Notes & Quirks](references/api-notes.md) <br>
- [ClawWatch CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and optional parsed JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON CLI output for structured summaries; respects market API rate limits and local watchlist state.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
