## Description: <br>
Eth Strategy analyzes public ETH/USDT market data with technical indicators and outputs heuristic direction, entry, stop-loss, and staged take-profit levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samary-xia](https://clawhub.ai/user/samary-xia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request heuristic crypto technical analysis and suggested signal levels for ETH/USDT or another supplied trading pair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic crypto trading signals may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis only and review them before using them in trading decisions. <br>
Risk: The skill contacts Binance for public market data. <br>
Mitigation: Run it only in environments where outbound public market-data requests to Binance are allowed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output an empty JSON object when no signal is generated.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
