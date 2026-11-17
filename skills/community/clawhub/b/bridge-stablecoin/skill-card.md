## Description:

Build USDC bridging workflows with Circle Bridge Kit SDK and Crosschain Transfer Protocol across EVM chains, Solana, and Circle Wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold and reason through USDC bridge integrations, including Circle Bridge Kit adapters, CCTP lifecycle handling, event handling, retries, and mainnet safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill examples involve signing credentials and transaction code for USDC bridge operations.

Mitigation: Use testnets and low-balance test wallets first, keep private keys and Circle secrets out of logs and source control, and use reviewed dependency versions.

Risk: Mainnet bridge transactions can move funds irreversibly if the chain, recipient, token, or amount is wrong.

Mitigation: Require explicit confirmation of source chain, destination chain, recipient, amount, and token before any mainnet bridge transaction.

## Reference(s):

- [Private Key Adapter (Viem + Solana Kit)](references/adapter-private-key.md)
- [Circle Wallets Adapter (Developer-Controlled Wallets)](references/adapter-circle-wallets.md)
- [Wagmi Adapter (Browser Wallets)](references/adapter-wagmi.md)
- [Circle Bridge Kit SDK](https://developers.circle.com/bridge-kit)
- [CCTP Documentation](https://developers.circle.com/cctp)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, environment variable, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction confirmation steps, security warnings, and retry guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
