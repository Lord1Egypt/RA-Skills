## Description: <br>
Access unsecured credit lines for AI agents on the Arc Network using the Credex Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capGoblin](https://clawhub.ai/user/capGoblin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to check credit status, borrow or repay USDC, manage liquidity provider positions, and bridge USDC between Arc Testnet and Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a raw wallet private key for live DeFi actions. <br>
Mitigation: Use a dedicated low-value or testnet wallet, keep the private key out of shared logs, and review commands before execution. <br>
Risk: Borrow, repay, approval, deposit, withdrawal, and bridge commands can trigger irreversible financial transactions. <br>
Mitigation: Manually confirm transaction intent, amount, destination chain, pool contract, and agent URL before running transaction commands. <br>
Risk: Misconfigured pool contract or agent service endpoints can route actions to unintended services or contracts. <br>
Mitigation: Verify CREDEX_POOL_ADDRESS and CREDEX_AGENT_URL before each run and use only local or trusted agent endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/capGoblin/credex-protocol) <br>
- [Credex Protocol Contract Reference](references/contracts.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON from CLI commands, with Markdown setup guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require wallet and RPC configuration and may submit financial transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
