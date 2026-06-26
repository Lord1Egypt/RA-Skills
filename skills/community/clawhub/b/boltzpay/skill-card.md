## Description: <br>
Pay for API data automatically - multi-protocol (x402 + L402 + MPP), multi-chain, streaming sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leventilo](https://clawhub.ai/user/leventilo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use BoltzPay to discover paid API endpoints, inspect prices, manage budgets, and fetch paid API data through the BoltzPay CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid fetches can spend real funds. <br>
Mitigation: Require explicit user approval before spending commands, review quotes first, set BOLTZPAY_DAILY_BUDGET and per-transaction limits, and prefer testnet or limited-scope funds where possible. <br>
Risk: Payment and wallet credentials are required for paid access. <br>
Mitigation: Store Coinbase and other payment secrets in a secrets manager and avoid exposing them in prompts, logs, shell history, or shared configuration files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/leventilo/boltzpay) <br>
- [BoltzPay documentation](https://boltzpay.ai) <br>
- [BoltzPay registry](https://status.boltzpay.ai) <br>
- [BoltzPay npm package](https://www.npmjs.com/package/@boltzpay/sdk) <br>
- [BoltzPay GitHub link from skill documentation](https://github.com/leventilo/boltzpay) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx for CLI execution; paid fetches require Coinbase wallet credentials, with optional Tempo, NWC, Stripe, and daily budget settings described in the artifact.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
