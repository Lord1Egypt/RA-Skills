## Description: <br>
A local-key swap planning and execution skill for quoting, validating, signing locally, broadcasting, monitoring, and recovering EVM swaps across cross-chain 1inch Fusion+, same-chain 1inch Fusion, and same-chain 1inch Aggregation Router v6 paths while keeping private keys on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galphaai](https://clawhub.ai/user/galphaai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to plan, validate, locally sign, submit, monitor, and recover EVM swap workflows while keeping wallet secrets out of chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides irreversible crypto wallet signing and swap execution. <br>
Mitigation: Use small amounts first, require exact plan review and explicit authorization, and keep all private keys, mnemonics, passwords, API keys, and hash-lock secrets out of chat and persisted artifacts. <br>
Risk: The reviewed package is missing helper scripts that its safety workflow references. <br>
Mitigation: Do not run referenced scripts, generate wallets, approve allowances, sign payloads, or broadcast transactions until the actual helper code is obtained from a verified source, reviewed, dependency-pinned, and tested. <br>
Risk: Routes may be incorrectly presented as gasless when approvals, native fees, or insufficient allowances still require a source-chain transaction. <br>
Mitigation: Confirm balances, allowances, permit support, spender addresses, fees, and the gasless verdict for each route before requesting user approval. <br>


## Reference(s): <br>
- [Execution Plan Schema](references/execution-plan-schema.md) <br>
- [Provider Adapter Notes](references/provider-adapters.md) <br>
- [Security Policy](references/security-policy.md) <br>
- [Sample Execution Plan](references/sample-plan.json) <br>
- [1inch Fusion Overview](https://help.1inch.com/en/articles/9842591-what-is-1inch-fusion-and-how-does-it-work) <br>
- [1inch Cross-Chain SDK](https://github.com/1inch/cross-chain-sdk) <br>
- [1inch Fusion Documentation](https://portal.1inch.dev/documentation/fusion/introduction) <br>
- [1inch Swap Quick Start](https://portal.1inch.dev/documentation/swap/quick-start) <br>
- [1inch Aggregation Protocol](https://docs.1inch.io/docs/aggregation-protocol/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON execution-plan summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans, commands, status summaries, and risk notes; real execution requires local signing and explicit user authorization.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
