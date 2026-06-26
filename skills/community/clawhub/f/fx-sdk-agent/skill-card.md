## Description: <br>
Use FX Protocol TypeScript SDK (fx-sdk) to query positions, build leverage operation transaction plans, bridge tokens between Base and Ethereum, and work with fxSAVE config, balances, redeem status, claim previews, deposits, withdrawals, and claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huwangtao123](https://clawhub.ai/user/huwangtao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate FX Protocol SDK workflows into agents or tools, generate runnable TypeScript transaction-planning code, and validate parameters for Ethereum mainnet and Base operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts may build or execute real blockchain transactions. <br>
Mitigation: Use plan-only or dry-run output first, then manually review every transaction target, value, data payload, approval, and route before using a wallet. <br>
Risk: Incorrect chain IDs, token addresses, recipient addresses, amounts, slippage, or approval targets can cause failed transactions or financial loss. <br>
Mitigation: Verify chain IDs, addresses, token constraints, bigint amount units, slippage bounds, and approval targets against trusted project documentation before execution. <br>
Risk: Dependency or RPC drift can change transaction behavior or returned routes. <br>
Mitigation: Pin and review dependencies, use trusted RPC endpoints, and re-query positions or balances after confirmations before taking further action. <br>


## Reference(s): <br>
- [FX Protocol Website](https://fx.aladdin.club/) <br>
- [FX SDK Repository](https://github.com/aladdindao/fx-sdk.git) <br>
- [Reference Index](references/README.md) <br>
- [SDK Playbook](references/sdk-playbook.md) <br>
- [Agent Adapter Example](references/agent-adapter-example.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript code blocks, command lists, validation checklists, and transaction plan summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run transaction routes, sequential execution guidance, and post-execution verification steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
