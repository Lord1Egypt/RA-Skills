## Description:

clawrtc helps agents mine RTC tokens by running hardware fingerprinting, RustChain network attestation, and wallet management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use clawrtc to install and run an RTC miner, attest real hardware to the RustChain network, and manage RTC or Coinbase Base wallet details for rewards and swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mining can run continuously, use CPU, contact external RustChain services, and optionally install a user-level background service.

Mitigation: Use dry-run and hash verification before installation, avoid `--service` unless persistent mining is intended, and monitor resource and network use.

Risk: Hardware attestation may transmit device identifiers such as hostname, MAC address, and hardware fingerprint data.

Mitigation: Run only on approved systems and networks after reviewing the disclosed attestation data and privacy tradeoffs.

Risk: Wallet handling can create local wallet files and private-key exports, and Coinbase wallet creation depends on CDP credentials.

Mitigation: Keep wallet files permission-restricted, prefer public-only exports, and protect CDP private key environment variables.

Risk: Security evidence flags under-disclosed telemetry and local wallet/service hardening concerns.

Mitigation: Review the package before installing, do not bypass prompts with unattended consent unless already approved, and avoid private-key export or persistent services without operational review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/clawrtc-pip)
- [PyPI package](https://pypi.org/project/clawrtc/)
- [npm package](https://www.npmjs.com/package/clawrtc)
- [RustChain](https://rustchain.org)
- [RustChain block explorer](https://rustchain.org/explorer)
- [RustChain agent wallets](https://rustchain.org/wallets.html)
- [Coinbase Developer Platform](https://portal.cdp.coinbase.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install, start, status, uninstall, wallet, Coinbase Base, and swap guidance.]

## Skill Version(s):

1.5.0 (source: server release metadata, pyproject.toml, package.json, clawrtc/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
