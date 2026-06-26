## Description: <br>
Provides optional pre-transaction token risk assessments for Solana and Base trades through paid, read-only Bitfence API checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilsbys](https://clawhub.ai/user/bilsbys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users operating on-chain use this skill before unfamiliar token swaps, purchases, liquidity provision, or staking to request a Bitfence risk report and decide whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid risk checks can spend small amounts of USDC on Base mainnet if invoked without clear user consent. <br>
Mitigation: Inform the user before the first paid check in a session, ask for consent, avoid repeated or batched checks, and keep wallet approval controls enabled for x402 payments. <br>
Risk: Contextual checks can share position size and portfolio size with Bitfence. <br>
Mitigation: Use the contextual endpoint only after explicit opt-in; otherwise use the token-only endpoint that sends only the chain and public token address. <br>
Risk: Risk reports are advisory, and API errors or low-confidence responses can leave uncertainty. <br>
Mitigation: Surface warnings, confidence limitations, circuit breakers, and errors to the user, then let the user choose whether to retry, proceed without the check, or abandon the action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bilsbys/bitfence) <br>
- [Bitfence website](https://bitfence.ai) <br>
- [Bitfence API root](https://api.bitfence.ai) <br>
- [Bitfence X profile](https://x.com/bitfenceai) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON API responses summarized as concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only advisory checks; paid x402 requests require user consent, and optional contextual checks may include position size and portfolio size only with explicit opt-in.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
