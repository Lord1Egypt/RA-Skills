## Description:

MCP server providing Base L2 DeFi tools for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to expose Base L2 DeFi, wallet, price, contract, and security-analysis tools through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mnemonic generation can expose wallet seed material to the remote service.

Mitigation: Do not use generated phrases for wallets that may hold real assets; treat every generated phrase as disclosed.

Risk: Contract code and wallet-analysis targets may be disclosed to third-party services.

Mitigation: Submit only data approved for third-party disclosure and avoid private contract source or sensitive wallet targets.

Risk: Wallet and DeFi features can affect high-value assets if connected to funded wallets.

Mitigation: Review the skill before installation and restrict use to controlled wallets and explicitly approved operations.

Risk: The Docker payment service has unsafe payment-verification and webhook-authentication behavior.

Mitigation: Do not expose it with real paid data until payment verification and webhook authentication are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manteclaw/skills/base-l2-agent-kit)
- [Skill-provided GitHub link](https://github.com/manteclaw/base-l2-agent-kit-mcp)
- [PyPI project](https://pypi.org/project/base-l2-agent-kit/)
- [MCP.so listing](https://mcp.so/server/base-l2-agent-kit)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Text and Markdown with inline JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tool responses may include wallet, token, gas, contract, quote, yield, audit, and mnemonic information from remote services.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, pyproject.toml, server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
