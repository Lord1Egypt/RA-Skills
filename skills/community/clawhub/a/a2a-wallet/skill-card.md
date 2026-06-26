## Description: <br>
Use the a2a-wallet CLI to interact with A2A agents, discover registry entries, send or stream messages, manage tasks, sign x402 payments, and manage local wallets. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ost006](https://clawhub.ai/user/ost006) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate the a2a-wallet CLI for A2A agent messaging, registry discovery, x402 payment signing, wallet setup, balance checks, faucet requests, and CLI configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation flow can install mutable remote code through a curl-to-shell command. <br>
Mitigation: Review and verify the installer before running it, and prefer pinned or release-verified artifacts where possible. <br>
Risk: Local wallet keys may be stored as plaintext files on disk. <br>
Mitigation: Use only fresh low-value wallets, never import a valuable wallet, and avoid storing significant assets in wallets managed by this tool. <br>
Risk: The CLI can sign payments and perform wallet, registry, faucet, configuration, and update actions. <br>
Mitigation: Require explicit user approval before every wallet creation, import, export, config change, CLI update, registry registration, faucet request, and payment-signing action. <br>
Risk: Custodial wallet security depends on a third-party provider and web service. <br>
Mitigation: Use custodial wallets only for small micro-payments and explain that key management is outside the user's direct control. <br>


## Reference(s): <br>
- [a2a-wallet repository](https://github.com/planetarium/a2a-x402-wallet) <br>
- [A2A x402 specification](https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2) <br>
- [a2a-wallet releases](https://github.com/planetarium/a2a-x402-wallet/releases/latest) <br>
- [Privy](https://privy.io) <br>
- [a2a-wallet installer script](https://raw.githubusercontent.com/planetarium/a2a-x402-wallet/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should include explicit user approval before wallet creation, wallet import or export, payment signing, registry registration, faucet requests, config changes, and CLI updates.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
