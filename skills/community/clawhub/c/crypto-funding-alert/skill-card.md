## Description: <br>
Real-time crypto funding rate scanner with smart alerts that finds negative funding rates for profitable long positions on Binance futures without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and crypto traders use this skill to scan Binance futures public market data for negative funding-rate signals, classify opportunities, and record scan history for later review. Its output should be treated as research support, not guaranteed trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto futures suggestions can be incorrect, stale, or unsuitable for a user's risk tolerance. <br>
Mitigation: Treat output as research, verify market conditions independently, and avoid using the recommendations as guaranteed risk controls. <br>
Risk: The skill contacts Binance public endpoints and saves local scan history. <br>
Mitigation: Install only where Binance network access and local JSONL history retention are acceptable; configure the output path when needed. <br>
Risk: Cron jobs or webhook integrations can create recurring scans or external alerts. <br>
Mitigation: Enable automation only when recurring monitoring is intended, and review webhook destinations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/crypto-funding-alert) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with ranked signal rows, recommended actions, and JSONL history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, contacts Binance public endpoints, and saves scan history locally by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
