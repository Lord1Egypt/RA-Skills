## Description: <br>
Track stock and crypto portfolios with CLI - real-time prices, P&L, dividend tracking, multiple portfolios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsoutar](https://clawhub.ai/user/rsoutar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage local stock and crypto portfolios, inspect current value and profit/loss, track dividends, and export portfolio data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores portfolio holdings locally and includes sell, remove, and delete operations that can change local portfolio records. <br>
Mitigation: Keep backups of data/portfolio.json before destructive operations and review requested portfolio changes before execution. <br>
Risk: The skill sends ticker and crypto symbols to external market-data providers for prices and dividend information. <br>
Mitigation: Use only when sharing symbol lookups with Yahoo Finance and CoinGecko is acceptable for the user's workflow. <br>
Risk: The optional web UI is intended for trusted local use. <br>
Mitigation: Run the web UI only on a trusted local machine and avoid exposing the localhost service to untrusted networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsoutar/claw-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tabular portfolio summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local portfolio data in data/portfolio.json and can optionally serve a localhost web UI.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
