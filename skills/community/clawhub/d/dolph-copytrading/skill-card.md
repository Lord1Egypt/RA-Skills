## Description: <br>
Mirror positions from top Polymarket traders using Simmer API with size-weighted aggregation across multiple wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to inspect and mirror selected Polymarket wallet positions through Simmer, starting with dry-run or simulated trading before enabling live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute live Polymarket trades when live mode is enabled. <br>
Mitigation: Start in dry-run or $SIM mode, review the proposed trades, and keep max trade and max run limits small before enabling live execution. <br>
Risk: Persistent configuration changes can affect future trading behavior. <br>
Mitigation: Review saved wallet lists, venue, position count, max trade size, and max trades per run before recurring or automated use. <br>
Risk: Providing wallet signing credentials enables SDK-managed live trading from the environment. <br>
Mitigation: Only provide wallet private key material in an environment approved for live trading and remove it when live execution is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-copytrading) <br>
- [Publisher profile](https://clawhub.ai/user/richducat) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [predicting.top](https://predicting.top) <br>
- [alphawhale.trade](https://alphawhale.trade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style text with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize wallet positions, trade plans, executed trades, skipped markets, account status, and persistent configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
