## Description: <br>
Produces Chinese-language BTC/ETH four-hour market recaps and manual OKX contract and spot-grid trading templates using the referenced crypto market analyzer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmzo](https://clawhub.ai/user/hmzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent for a Chinese-language BTC/ETH trading brief with data-quality gates, observation-only cases, and manual OKX contract and spot-grid parameters. The output is decision support and requires independent price verification before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce crypto leverage and grid-trading parameters that may be incorrect, stale, or unsuitable for a user's risk tolerance. <br>
Mitigation: Review the referenced analyzer dependency, verify market prices independently, and treat the output as decision support rather than financial advice. <br>
Risk: The skill relies on a disclosed local market-data analyzer, so stale or incomplete data can affect generated trading templates. <br>
Mitigation: Use the skill's data-availability gates and pause execution when data is incomplete, stale, or below the configured candle-count thresholds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hmzo/crypto-4h-trade-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Chinese Markdown with manual OKX contract and spot-grid templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes data-quality gates, risk disclaimers, and manually entered trading parameters; does not place trades.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
