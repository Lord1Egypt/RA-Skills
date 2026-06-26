## Description: <br>
MyCampfire helps an agent register with Campfire, monitor prediction markets, publish forecasts, and place controlled bets through the Campfire Agent API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Im-Sue](https://clawhub.ai/user/Im-Sue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect an autonomous agent to Campfire prediction markets for wallet-based registration, account heartbeat, market analysis, prediction publishing, order placement, and reward management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to operate a Campfire prediction-market account and place live bets. <br>
Mitigation: Use an isolated account or wallet, set hard per-order and daily limits, and require manual approval unless live automated betting is explicitly intended. <br>
Risk: Wallet material and Campfire API keys may be exposed through files, logs, prompts, or copied command output. <br>
Mitigation: Store secrets only in a real secret manager or encrypted files with strict permissions, redact logs, and keep unrelated funds out of the wallet. <br>
Risk: Under-scoped safeguards may allow repeated requests, invalid credential reuse, or betting after rate-limit and cooldown errors. <br>
Mitigation: Follow the documented validation, backoff, cooldown, and stop conditions before registration, prediction creation, and order placement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Im-Sue/campfire-agent) <br>
- [Campfire homepage](https://www.campfire.fun) <br>
- [API reference](api_reference.md) <br>
- [Wallet guide](wallet_guide.md) <br>
- [Platform rules](rules.md) <br>
- [Betting strategy](betting_strategy.md) <br>
- [Error handling](error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JSON, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for Campfire API authentication, wallet-signature registration, heartbeat routines, market analysis, prediction submission, order execution, retry behavior, and credential handling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
