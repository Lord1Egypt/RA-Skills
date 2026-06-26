## Description: <br>
Run user-facing EasyClaw DEX actions from a self-contained skill folder for order submission, wallet and margin checks, backend queries, realtime monitoring, and agent or strategy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ice-coldbell](https://clawhub.ai/user/ice-coldbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and EasyClaw users use this skill to check wallet, margin, position, order, fill, history, chart, and orderbook data, and to submit or automate EasyClaw DEX orders. It also supports authenticated agent, strategy, risk, and kill-switch controls when the user provides the required credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Solana wallet and API token to place real or automated trades and manage EasyClaw agents. <br>
Mitigation: Use a dedicated low-balance or devnet wallet, keep API tokens scoped and revocable, start with dry-run, and review every backend or autotrade command before live execution. <br>
Risk: Automated trading can continue placing orders from realtime signals if limits are not configured. <br>
Mitigation: Set max order, cooldown, margin, confidence, and kill-switch controls before enabling live autotrade. <br>
Risk: Incorrect wallet, RPC, backend, or program ID configuration can direct actions to unintended accounts or services. <br>
Mitigation: Confirm KEYPAIR_PATH, RPC endpoints, backend URLs, and program IDs before placing orders. <br>


## Reference(s): <br>
- [EasyClaw User DEX Env Reference](references/dex-env.md) <br>
- [EasyClaw skill homepage](https://github.com/ice-coldbell/easyclaw/tree/main/easyclaw-skill) <br>
- [ClawHub skill page](https://clawhub.ai/ice-coldbell/easyclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-capable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands can read local wallet configuration, call Solana RPC or EasyClaw backend services, write local .env and strategy files, and submit or automate orders.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
