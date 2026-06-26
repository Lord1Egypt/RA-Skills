## Description: <br>
Deploy an agent token with a Uniswap V4 pool — handles pool creation with configurable hooks (anti-snipe, dynamic fees, revenue share), initial liquidity bootstrapping, LP locking, and post-deployment monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and teams launching agent tokens use this skill to configure a Uniswap V4 pool, bootstrap initial liquidity, lock LP positions, and monitor launch activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates irreversible crypto transactions for Uniswap pool creation and liquidity operations. <br>
Mitigation: Use a wallet that requires manual signing and verify every contract address, hook, approval, amount, slippage setting, recipient, and LP lock duration before any transaction. <br>
Risk: User approval and wallet-signing boundaries are not clearly defined in the skill documentation. <br>
Mitigation: Do not grant the agent unattended authority over funds; require explicit user confirmation before broadcasts or approvals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/deploy-agent-token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown deployment report with pool, liquidity, LP lock, and early monitoring details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human review and wallet signing before irreversible transaction execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
