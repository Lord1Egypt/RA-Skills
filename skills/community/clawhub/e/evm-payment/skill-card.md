## Description:

Generate EIP-681 Ethereum payment links and QR codes for any EVM chain, including Base, Ethereum, Arbitrum, Optimism, and Polygon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to create local payment requests, invoices, donation links, QR codes, and wallet links for ETH and ERC-20 payments on supported EVM networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate invalid or misleading payment requests if recipient addresses, token symbols, amounts, networks, or token configuration are wrong.

Mitigation: Independently verify recipient addresses, amounts, tokens, networks, and generated wallet links before sharing or using them.

Risk: QR generation can overwrite a caller-chosen output file path.

Mitigation: Write QR files only to safe new paths in a disposable or controlled directory.

Risk: The server security guidance flags Ethereum DAI output as unreliable until configuration is corrected.

Mitigation: Avoid relying on Ethereum DAI payment output unless the token configuration has been reviewed and corrected.

Risk: QR generation requires third-party Python packages.

Mitigation: Install qrcode and pillow in an isolated Python environment when QR generation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bevanding/skills/evm-payment)
- [Publisher profile](https://clawhub.ai/user/bevanding)
- [MetaMask deep link examples](https://metamask.app.link/send/...)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Human-readable CLI text, JSON, EIP-681 links, MetaMask deep links, transaction fields, and optional PNG QR code files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated locally from caller-provided recipient, amount, token, network, and optional QR path.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
