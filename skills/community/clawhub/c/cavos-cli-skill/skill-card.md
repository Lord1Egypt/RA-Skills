## Description: <br>
Interact with the Cavos CLI for Starknet wallet operations. Use for transfers, approvals, contract calls, session management, and transaction monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adrianvrj](https://clawhub.ai/user/adrianvrj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide an agent through Cavos CLI workflows for Starknet wallet sessions, balances, transfers, approvals, contract reads and writes, simulations, multicalls, and transaction-status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through wallet transfers, approvals, execute calls, and multicalls. <br>
Mitigation: Manually confirm the active wallet, network, recipient or spender, token, amount, contract address, calldata, and expected result before any transaction-producing command. <br>
Risk: Approval commands can grant spending authority that exceeds the immediate task. <br>
Mitigation: Avoid unlimited approvals, approve only the needed amount and token, and revoke or expire access when the workflow is complete. <br>
Risk: Imported Cavos sessions can enable authenticated wallet operations. <br>
Mitigation: Import session tokens only from trusted Cavos dashboard sessions, check session status before use, and revoke or expire sessions after completing the task. <br>
Risk: Contract execution and multicall calldata can produce unintended on-chain effects. <br>
Mitigation: Prefer simulation before execution and review contract address, entrypoint, calldata, and expected result before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adrianvrj/cavos-cli-skill) <br>
- [Cavos Agent Dashboard](https://agent.cavos.xyz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with Cavos CLI shell commands and JSON-oriented command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and an imported Cavos session token for authenticated wallet operations; commands should use --json where supported.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
