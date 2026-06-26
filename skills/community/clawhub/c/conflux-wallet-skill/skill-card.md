## Description: <br>
Self-sovereign EVM wallet for AI agents that can create a local crypto wallet, check balances, send ETH or ERC20 tokens, swap tokens, and interact with smart contracts across supported EVM chains. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[pana](https://clawhub.ai/user/pana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent manage a self-hosted EVM wallet workflow, including wallet setup, balance checks, token transfers, swaps, and contract calls. The artifact describes this as exploratory and requires careful user confirmation before any irreversible transaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs unpinned external code that can handle private keys and irreversible crypto transactions. <br>
Mitigation: Review or pin the GitHub code before use, install only from trusted sources, and use a new low-balance wallet for testing. <br>
Risk: The local wallet file contains sensitive credentials and loss or disclosure can lead to loss of funds. <br>
Mitigation: Protect and back up ~/.cfx-wallet.json, never share the private key or wallet file, and avoid reinitializing the wallet over an existing funded wallet. <br>
Risk: Transfers, swaps, token approvals, and write contract calls are irreversible and may use the wrong chain, token, amount, or spender. <br>
Mitigation: Manually verify chain, recipient, token, amount, approvals, gas, and quote details before confirming any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pana/conflux-wallet-skill) <br>
- [Project homepage](https://github.com/conflux-fans/conflux-wallet-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [viem](https://viem.sh) <br>
- [Odos](https://odos.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be run with --json when available; transfers, swaps, approvals, and write contract calls require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
