## Description: <br>
Run the CCTP relay to burn USDC on a source chain and mint on a destination chain, returning verifiable receipts for multichain agent-to-agent settlement with optional Moltbook discovery and integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nativ3ai](https://clawhub.ai/user/nativ3ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to prepare and run a CCTP-based USDC bridge workflow for agent-to-agent settlement across supported chains. It also covers optional counterparty discovery and integration modules before settlement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can move funds because it requires a wallet private key for CCTP relay transactions. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit approval of source chain, destination chain, amount, recipient, fees, and contract addresses before signing. <br>
Risk: The relay code referenced by the skill is not included in the artifact evidence, so the implementation cannot be reviewed from this card context alone. <br>
Mitigation: Inspect and pin the relay source code before installation or use, and verify Circle CCTP contract addresses and domain IDs against trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nativ3ai/agentic-commerce-relay) <br>
- [Moltbook](https://www.moltbook.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash command snippets and JSON receipt fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RPC URLs, a wallet private key, CCTP contract settings, and transaction approval before signing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
