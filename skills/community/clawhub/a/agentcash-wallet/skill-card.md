## Description: <br>
Manage an agentcash wallet and call x402-protected APIs with automatic USDC payment on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fmhall](https://clawhub.ai/user/fmhall) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to check an agentcash wallet balance, redeem invite codes, fund a Base USDC wallet, discover x402 API pricing, and make paid API requests through the agentcash CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent spend from a persistent funded USDC wallet when making paid API calls. <br>
Mitigation: Keep the wallet balance low, require explicit approval before each paid request, and verify the destination and price before execution. <br>
Risk: Requests to third-party APIs may include sensitive, regulated, or private business data. <br>
Mitigation: Do not submit such data unless the API terms have been reviewed and the user is authorized to share it. <br>
Risk: Installing or running the agentcash CLI depends on the external npm package selected by the environment. <br>
Mitigation: Inspect the package or pin a trusted version before use in higher-trust environments. <br>
Risk: Funds sent using the wrong network or token may be lost. <br>
Mitigation: Confirm funding uses USDC on Base (eip155:8453) before depositing to the wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fmhall/agentcash-wallet) <br>
- [Getting Started](artifact/rules/getting-started.md) <br>
- [StableEnrich API origin](https://stableenrich.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can initiate paid USDC transactions through agentcash; use --format json when machine-readable CLI output is needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
