## Description: <br>
Build natural-language crypto agents, web3 assistants, trading bots, blockchain MCPs, or agent plugins that read EVM chain state, compose wallet requests, simulate transactions, and sign user-approved transactions through the Aomi CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceciliaz030](https://clawhub.ai/user/ceciliaz030) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Transact to build or run crypto agents that inspect EVM state, queue wallet requests, simulate transaction batches, and sign transactions through the Aomi CLI with explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signed blockchain transactions can move assets and may be hard or impossible to reverse. <br>
Mitigation: Verify the chain, recipient, amounts, approvals, and simulation results before signing; sign only after explicit user approval. <br>
Risk: Wallet keys, API keys, and account-abstraction credentials are sensitive if configured for CLI use. <br>
Mitigation: Provide credentials only when intentionally configuring them; the skill should not fabricate, derive, log, or echo credential values. <br>
Risk: Third-party quotes, routes, or protocol data can influence transaction calldata. <br>
Mitigation: Use fork simulation and drain-vector checks before signing, and treat failed or blocked simulations as stop conditions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ceciliaz030/aomi-transact) <br>
- [Aomi Transact source homepage](https://github.com/aomi-labs/skills/tree/main/aomi-transact) <br>
- [Aomi CLI package](https://www.npmjs.com/package/@aomi-labs/client) <br>
- [Security posture](artifact/SECURITY.md) <br>
- [Command Reference](artifact/references/commands.md) <br>
- [Workflows](artifact/references/workflows.md) <br>
- [Gotchas, Hard Rules, and Security Model](artifact/references/gotchas.md) <br>
- [Account Abstraction Reference](artifact/references/account-abstraction.md) <br>
- [Apps Reference](artifact/references/apps.md) <br>
- [Flow Examples](artifact/references/examples.md) <br>
- [Session Reference](artifact/references/session.md) <br>
- [Drain Vectors](artifact/references/drain-vectors.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference pending transaction IDs, simulation results, transaction hashes, chain settings, wallet state, and credential handle names; credential values should not be echoed.] <br>

## Skill Version(s): <br>
0.10.0 (source: server release metadata; artifact frontmatter reports 0.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
