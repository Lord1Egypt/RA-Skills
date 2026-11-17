## Description:

Guide users through installing, signing in to, connecting, and troubleshooting FreeGuard VPN with the official FreeGuard CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jojocrystal](https://clawhub.ai/user/jojocrystal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get plain-language guidance for installing the FreeGuard CLI, signing in, checking subscription status, connecting to VPN locations, and troubleshooting CLI-reported issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes login command examples that can carry tokens, subscription URLs, email addresses, or verification codes.

Mitigation: Prefer the FreeGuard CLI's interactive or browser-based login flow, and do not paste tokens, verification codes, payment details, or other secrets into chat.

Risk: The skill depends on a vendor CLI installation path that is not pinned to a specific version.

Mitigation: Install only when the user trusts the FreeGuard CLI source, verify the Homebrew formula or published release checksum, and run diagnostics with the CLI before connecting.

Risk: System-wide VPN protection may change low-level network routing and can request administrator approval.

Mitigation: Use standard non-elevated connection mode by default and discuss system-wide protection only when the user explicitly asks for it.

## Reference(s):

- [FreeGuard homepage](https://freeguardvpn.com)
- [ClawHub skill page](https://clawhub.ai/jojocrystal/skills/freeguard-setup)
- [Package provenance notes](references/provenance.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; the skill does not produce executable files or store credentials.]

## Skill Version(s):

0.8.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
