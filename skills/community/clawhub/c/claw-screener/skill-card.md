## Description: <br>
Stock screener combining Williams %R oversold signals with Warren Buffett-style fundamental analysis. Supports US (S&P 500) and Thai (SET) markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsoutar](https://clawhub.ai/user/rsoutar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to screen US and Thai equities for oversold technical signals, Buffett-style fundamental strength, compounder characteristics, and watchlist alerts. Outputs are informational screening results and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to public market-data sources and writes local watchlist and cache files. <br>
Mitigation: Confirm that this behavior is acceptable before installation and review the configured file locations for local persistence. <br>
Risk: The installation documentation includes pipe-to-shell Bun installer guidance. <br>
Mitigation: Install Bun through a trusted channel or inspect the installer before running it. <br>
Risk: Stock screening results can be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis only and validate financial decisions independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsoutar/claw-screener) <br>
- [Bun runtime installation](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Text, JSON, Telegram-ready Markdown, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local watchlist and cache files; some full-universe scans can take 20-30+ minutes on an uncached first run.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
