## Description: <br>
Pay for anything with USDC - virtual cards for any online checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawallex-tech](https://clawhub.ai/user/clawallex-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use Clawallex to set up a Clawallex account, check USDC balances, create one-time or reloadable virtual cards, refill cards, and inspect card or transaction status from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create USDC-funded virtual cards, subscriptions, refills, and card-control changes that may spend funds. <br>
Mitigation: Require explicit user approval before every payment, subscription, refill, and card-control change, and verify wallet balance before spending. <br>
Risk: Account credentials are stored locally on the machine running the agent. <br>
Mitigation: Use a dedicated or limited API key when possible and protect the local Clawallex credential directory on shared machines. <br>
Risk: Card details can include sensitive PAN and CVV data for checkout use. <br>
Mitigation: Use sensitive card details only to fill checkout forms, never display PAN or CVV in chat, and show only masked card numbers to users. <br>


## Reference(s): <br>
- [Clawallex on ClawHub](https://clawhub.ai/clawallex-tech/clawallex) <br>
- [Clawallex dashboard settings](https://app.clawallex.com/dashboard/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [JSON command output with markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return success or error JSON; payment and card operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
