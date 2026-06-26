## Description: <br>
Provides real-time China A-share quotes, intraday volume distribution analysis, main-fund movement signals, limit-order context, and portfolio profit/loss management for Shanghai, Shenzhen, and Beijing exchange stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A-share market data, inspect minute-level volume patterns, identify documented trading-signal heuristics, and manage saved portfolio positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package identity and portfolio storage path do not match the registry listing, which may cause this skill to share or alter another a-stock-analysis skill's portfolio file. <br>
Mitigation: Inspect or back up ~/.clawdbot/skills/a-stock-analysis/portfolio.json before use, and avoid running it alongside another a-stock-analysis skill until the namespace mismatch is resolved. <br>
Risk: The skill uses live market-data endpoints and may return delayed, unavailable, or trading-hours-dependent values. <br>
Mitigation: Treat quote and signal output as informational analysis, confirm important market data with an authoritative source, and avoid relying on it as sole financial advice. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/litiao1224/a-stock-analysis-conflict) <br>
- [Publisher profile](https://clawhub.ai/user/litiao1224) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina Finance quote API endpoint](https://hq.sinajs.cn/list={codes_str}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Terminal text and optional JSON output from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read live market data from Sina Finance and may create or update a local portfolio JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
