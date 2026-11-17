## Description:

This ClawHub release disables the Bitget Wallet skill, so wallet, swap, market-data, token-info, security-audit, and trading operations are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunbin0908](https://clawhub.ai/user/xunbin0908)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can install this release as a disabled placeholder for the Bitget Wallet skill. Normal wallet, swap, market-data, token-info, security-audit, and trading operations are unavailable until the skill is enabled or updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains wallet custody, transaction signing, swap, and payment flows that can move funds if enabled.

Mitigation: Install only when that capability is intended, use a dedicated low-balance wallet, and require review of every decoded transaction or payment before signing.

Risk: Private keys passed through command-line arguments or broad environment variables can leak through shell history, process listings, logs, or agent context.

Mitigation: Use secure storage and narrow in-memory handling for keys; avoid command-line private-key arguments and broad environment variables.

Risk: Automatic x402 payment execution can spend funds on untrusted URLs.

Mitigation: Do not use x402 automatic payment mode with untrusted URLs; require user review and spending limits for payment requests.

Risk: The artifact describes a main-branch self-update path that could change behavior after installation.

Mitigation: Avoid self-updating from the main branch unless the new release has been separately verified.

Risk: This specific ClawHub release is disabled, while artifact files still describe operational wallet and trading behavior.

Mitigation: Treat the operational artifact behavior as unavailable for version 1.0.0 unless the skill is explicitly enabled or updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xunbin0908/skills/bitget-wallet-skill-disabled)
- [Bitget Wallet API documentation](https://web3.bitget.com/en/docs)
- [Artifact README](artifact/README.md)
- [Commands reference](artifact/docs/commands.md)
- [Swap domain knowledge](artifact/docs/swap.md)
- [Wallet and signing domain knowledge](artifact/docs/wallet-signing.md)
- [x402 payments domain knowledge](artifact/docs/x402-payments.md)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown or plain text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [This disabled release does not process wallet, swap, market-data, token-info, security-audit, or trading operations.]

## Skill Version(s):

1.0.0 (source: ClawHub server release metadata; artifact frontmatter reports 2026.3.12-1 and artifact changelog top entry reports 2026.3.13-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
