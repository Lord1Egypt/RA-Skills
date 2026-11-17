## Description:

Local-key swap planning and execution skill. Cross-chain (1inch Fusion+, gasless), same-chain gasless (1inch Fusion), and same-chain paid (1inch Aggregation Router v6) paths are bundled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galphaai](https://clawhub.ai/user/galphaai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to quote, validate, locally sign, broadcast, monitor, or recover EVM swap workflows while keeping private keys on the user's machine. It is intended for cross-chain 1inch Fusion+, same-chain 1inch Fusion, and same-chain Aggregation Router execution paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path depends on unreviewed external helper code for wallet and trading operations.

Mitigation: Install only from a pinned, reviewed release or commit that includes the actual scripts, dependency manifests, lockfiles, and tests.

Risk: Real swap execution can expose funds to irreversible blockchain, signing, allowance, or route-selection errors.

Mitigation: Before using real funds, verify the helper code locally, use a low-balance wallet or hardware-backed signer, and require exact plan-hash approval before any signature or broadcast.

Risk: Private keys, mnemonics, hash-lock secrets, bearer tokens, or provider responses could leak if handled through chat or saved artifacts.

Mitigation: Never paste secrets into chat, use local-only signing or keystore workflows, and persist only redacted non-secret audit artifacts.

## Reference(s):

- [Gasless Crosschain Executor on ClawHub](https://clawhub.ai/galphaai/skills/gasless-crosschain-executor)
- [Execution plan schema](references/execution-plan-schema.md)
- [Provider adapter notes](references/provider-adapters.md)
- [Security policy](references/security-policy.md)
- [Sample execution plan](references/sample-plan.json)
- [1inch Fusion documentation](https://help.1inch.com/en/articles/9842591-what-is-1inch-fusion-and-how-does-it-work)
- [1inch Cross-Chain SDK](https://github.com/1inch/cross-chain-sdk)
- [1inch Fusion SDK](https://github.com/1inch/fusion-sdk)
- [1inch Swap API quick start](https://portal.1inch.dev/documentation/swap/quick-start)
- [1inch Aggregation Protocol documentation](https://docs.1inch.io/docs/aggregation-protocol/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON execution-plan snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should present normalized execution plans, plan hashes, route risks, user-approval requirements, and non-secret audit details.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
