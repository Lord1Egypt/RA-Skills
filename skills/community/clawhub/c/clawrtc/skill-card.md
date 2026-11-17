## Description:

ClawRTC helps an agent install and manage a RustChain RTC mining client, wallet, and signed RTC transfer commands tied to physical-device attestation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use ClawRTC to configure RTC mining on real hardware, inspect miner status, manage wallets, and submit signed pay, tip, gas, or settlement transfers. It is intended for users who deliberately want a hardware-fingerprinted mining and wallet workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security evidence flags wallet-linked hardware fingerprinting, MAC and hostname collection, cloud metadata probes, and contradictions with stated privacy promises.

Mitigation: Install only on an approved physical host without sensitive credentials, review the data disclosure before mining, and avoid cloud hosts unless the collection behavior is acceptable.

Risk: The release security evidence calls out a plaintext miner endpoint and unresolved TLS verification concerns, including BCOS admin-key exposure risk.

Mitigation: Do not use BCOS certification or admin keys until TLS verification and disclosure issues are fixed, and prefer test nodes or non-sensitive accounts when evaluating transfers.

Risk: The release security evidence notes hidden install telemetry and optional auto-start service behavior that users should review before installation.

Mitigation: Use dry-run and verification modes first, inspect the generated service configuration, and enable background service mode only after explicit approval.

## Reference(s):

- [ClawRTC Skill Page](https://clawhub.ai/scottcjn/skills/clawrtc)
- [RustChain Network](https://rustchain.org)
- [RustChain Block Explorer](https://rustchain.org/explorer)
- [BCOS Verification](https://rustchain.org/bcos/)
- [PyPI Package](https://pypi.org/project/clawrtc/)
- [npm Package](https://www.npmjs.com/package/clawrtc)
- [Coinbase CDP Portal](https://portal.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI commands, configuration steps, and status or transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet addresses, signed transfer payload previews, miner status, BCOS scan output, and install or uninstall instructions.]

## Skill Version(s):

1.9.0 (source: server release metadata, pyproject.toml, package.json; clawrtc/__init__.py reports 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
