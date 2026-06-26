## Description: <br>
Everclaw helps OpenClaw agents route inference through the Morpheus decentralized network with gateway setup, local proxy tooling, wallet-backed sessions, and open-source-first model fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DavidAJohnston](https://clawhub.ai/user/DavidAJohnston) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Everclaw to configure persistent OpenClaw inference through Morpheus gateway or local P2P paths, including model routing, proxy setup, session management, and wallet-backed access when enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent infrastructure and wallet-backed inference can make durable system and financial changes. <br>
Mitigation: Install only when that behavior is intended, prefer gateway-only setup if local staking is unnecessary, and review launchd and power-management changes before enabling always-on mode. <br>
Risk: One-line install and remote reinstall paths can execute fetched code. <br>
Mitigation: Prefer manual review, pinned installs, and inspected scripts over curl-piped execution. <br>
Risk: Wallet export, token swaps, and approvals can expose keys or create unintended on-chain spend authority. <br>
Mitigation: Avoid export-key except in a controlled terminal, set explicit swap slippage and approval amounts, and use the gateway path when wallet staking is not required. <br>
Risk: Repository-rewrite utilities may modify working copies or history outside the core inference workflow. <br>
Mitigation: Avoid running repository-rewrite scripts unless that operation is intentional and backups have been reviewed. <br>
Risk: Bootstrap and monitoring flows include device-fingerprinting and networked service checks. <br>
Mitigation: Review bootstrap behavior and prefer user-owned API keys when device-identifying bootstrap flows are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DavidAJohnston/everclaw-inference) <br>
- [Publisher profile](https://clawhub.ai/user/DavidAJohnston) <br>
- [Everclaw homepage](https://everclaw.com) <br>
- [Morpheus](https://mor.org) <br>
- [Morpheus API app](https://app.mor.org) <br>
- [Acquiring MOR](references/acquiring-mor.md) <br>
- [API reference](references/api.md) <br>
- [Economics reference](references/economics.md) <br>
- [Models reference](references/models.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose install, setup, wallet, proxy, and diagnostic commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.10.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
