## Description: <br>
Builds USDC bridging workflows with Circle Bridge Kit SDK and Crosschain Transfer Protocol (CCTP) across EVM chains, Solana, and Circle Wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add USDC bridge flows with Circle Bridge Kit, including adapter setup, transfer execution, event handling, error recovery, retry behavior, and forwarding-service configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys, Circle API keys, and entity secrets are required for some bridge flows and could expose funds if stored or logged unsafely. <br>
Mitigation: Keep secrets out of source control and logs, use environment variables or a secrets manager, and start with isolated low-balance test wallets. <br>
Risk: Bridge transactions can move real funds across chains and may be difficult or impossible to reverse after submission. <br>
Mitigation: Require explicit confirmation of source chain, destination chain, recipient, token, and amount before any production transfer. <br>
Risk: Dependency or configuration drift can affect bridge behavior in applications that integrate the SDK. <br>
Mitigation: Pin dependencies in the integrating project and review bridge configuration before deployment. <br>


## Reference(s): <br>
- [Private Key Adapter](references/adapter-private-key.md) <br>
- [Circle Wallets Adapter](references/adapter-circle-wallets.md) <br>
- [Wagmi Adapter](references/adapter-wagmi.md) <br>
- [Circle Bridge Kit SDK](https://developers.circle.com/bridge-kit) <br>
- [CCTP Documentation](https://developers.circle.com/cctp) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, chain, recipient, amount, fee, retry, and environment-variable guidance for bridge implementations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
