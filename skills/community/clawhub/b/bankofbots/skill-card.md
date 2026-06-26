## Description: <br>
Trust layer for agentic commerce. Build a BOB Score from on-chain payment proofs and x402 receipts, then borrow USDC credit lines based on your score. Non-custodial - BOB never holds your funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bankofbotsandy](https://clawhub.ai/user/bankofbotsandy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to Bank of Bots, manage agent identity and wallets, submit payment proofs, track BOB Score, operate governed treasury payments, and request or repay USDC loans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad real-money wallet, loan, treasury, and command-queue authority. <br>
Mitigation: Install it only for trusted agents, tightly scope BOB_API_KEY, and require explicit human approval for transfers, wallet sweeps, loan acceptance or repayment, webhook changes, and API-key changes. <br>
Risk: The skill depends on a separate bob CLI for wallet signing and privileged finance actions. <br>
Mitigation: Verify the CLI source and checksums before use, keep the CLI current, and run setup checks such as bob auth me, bob wallet list, bob agent passport-get, and bob doctor before funding or spending. <br>
Risk: Automatic heartbeat or inbox processing can execute privileged operator commands without enough review. <br>
Mitigation: Avoid automatic privileged command processing, or gate inbox actions with explicit approval before processing transfers, wallet provisioning, loan actions, kill switches, or key rotation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bankofbotsandy/bankofbots) <br>
- [BOB homepage](https://bankofbots.ai) <br>
- [BOB API docs](https://api.bankofbots.ai/docs) <br>
- [Agent setup guide](https://bankofbots.ai/docs/agent-setup) <br>
- [npm package](https://www.npmjs.com/package/@bankofbots/skill) <br>
- [CLI releases and checksums](https://github.com/bankofbots/bob-cli/releases/latest) <br>
- [BOB CLI command reference](artifact/references/commands.md) <br>
- [BOB CLI error recovery](artifact/references/errors.md) <br>
- [BOB Score proof submission](artifact/references/proofs.md) <br>
- [BOB Score tiers and credit events](artifact/references/scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command blocks and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOB_API_KEY and BOB_AGENT_ID; BOB_API_URL is optional.] <br>

## Skill Version(s): <br>
0.58.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
