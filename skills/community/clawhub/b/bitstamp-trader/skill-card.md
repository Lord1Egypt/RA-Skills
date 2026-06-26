## Description: <br>
Bitstamp Trader helps agents use a local Bitstamp CLI to inspect crypto markets and account data, simulate trades by default, and place explicit live spot orders with safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhen08](https://clawhub.ai/user/zhen08) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a local Bitstamp trading helper for market checks, balance review, order management, dry-run trade review, and explicitly approved live spot trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can place real Bitstamp trades when API keys are present and the user deliberately runs live commands. <br>
Mitigation: Use a dedicated Bitstamp API key with no withdrawal permission, enable IP whitelisting, keep dry-run as the normal workflow, and review every dry-run before any --live command. <br>
Risk: Local audit and configuration files may expose trading activity, safety limits, or operational history. <br>
Mitigation: Protect local config directories and periodically clear or rotate audit and configuration files when appropriate. <br>
Risk: Unexpected market movement, stale inputs, or an incorrect market pair could lead to an unintended trade. <br>
Mitigation: Keep order-size, daily-volume, price-deviation, allowed-market, confirmation, and kill-switch guardrails enabled and review command output before proceeding. <br>


## Reference(s): <br>
- [Safety Architecture](references/safety.md) <br>
- [Bitstamp API Reference](references/api-reference.md) <br>
- [Bitstamp Trader on ClawHub](https://clawhub.ai/zhen08/bitstamp-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, audit, daily-volume, and kill-switch files under BITSTAMP_CONFIG_DIR or ~/.config/bitstamp-trader.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
