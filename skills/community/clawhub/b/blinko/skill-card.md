## Description: <br>
Play Blinko on-chain Plinko headlessly on Abstract chain, including game stats, leaderboards, honey rewards, API authentication, on-chain game creation, simulation, and settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tolibear](https://clawhub.ai/user/tolibear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to play Blinko games from a hot wallet, inspect account game history, check leaderboards, and view honey balances on Abstract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses hot-wallet authority to sign on-chain transactions that can spend real ETH and incur gas costs. <br>
Mitigation: Install only with a dedicated low-balance wallet, review commands before execution, confirm transaction amounts and destination contracts, and avoid autonomous use without strict confirmations and spending limits. <br>


## Reference(s): <br>
- [ClawHub Blinko listing](https://clawhub.ai/tolibear/blinko) <br>
- [Blinko website](https://blinko.gg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with command examples and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WALLET_PRIVATE_KEY for play actions; stats commands can run with a wallet address.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
