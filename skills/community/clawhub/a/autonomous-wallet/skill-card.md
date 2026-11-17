## Description:

Helps agents operate an autonomous crypto wallet through natural-language blockchain intents, wallet configuration, self-healing transaction handling, and guardian-based recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to set up and guide wallet actions such as balance checks, transfers, swaps, staking, DeFi automation, recovery setup, and safety configuration across EVM networks. It is most relevant when an agent needs command, code, or configuration guidance for local wallet operations that may control real funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that expose wallet secrets to a globally installed npm package.

Mitigation: Review the npm package source and release provenance, pin the package version, and avoid pasting real mnemonics or private keys into commands or exported environment variables.

Risk: Generated commands can move real funds through transfers, approvals, staking, swaps, or recovery operations.

Mitigation: Use a disposable testnet wallet first and require simulation plus explicit human approval before any mainnet transaction or recovery action.

Risk: Local wallet automation may grant broad signing authority to an agent or CLI session.

Mitigation: Prefer hardware-wallet or isolated signing flows, enforce spending limits, and keep recovery guardians and timelocks reviewed before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/autonomous-wallet)
- [Publisher profile](https://clawhub.ai/user/zhenstaff)
- [GitHub repository listed in artifact](https://github.com/ZhenRobotics/openclaw-autonomous-wallet)
- [npm package listed in artifact](https://www.npmjs.com/package/openclaw-autonomous-wallet)
- [Documentation listed in artifact](https://docs.openclaw.ai/wallet)
- [Issue tracker listed in artifact](https://github.com/ZhenRobotics/openclaw-autonomous-wallet/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TypeScript snippets, JSON configuration examples, and structured JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet secrets, RPC endpoints, transaction intents, recovery settings, and safety configuration that require human review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
