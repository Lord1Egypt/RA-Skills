## Description:

A Cashu ecash wallet CLI for Bitcoin and Lightning payments. Use when managing Cashu tokens, sending/receiving payments via Lightning (bolt11) or ecash, handling HTTP 402 X-Cashu payment requests, or viewing wallet history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[egge21m](https://clawhub.ai/user/egge21m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Cashu wallet operations, Bitcoin and Lightning payments, HTTP 402 X-Cashu settlement flows, mints, daemon status, and wallet history through the cocod CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill with real wallet funds can expose or spend value if payment commands run without user review.

Mitigation: Ask for explicit permission before any spend command and preview payable requests before handling them whenever possible.

Risk: Wallet mnemonics, passphrases, local wallet files, and transferable Cashu tokens are sensitive.

Mitigation: Do not paste, print, or log wallet secrets in agent-visible commands; use protected secret-entry flows and expose only explicitly requested safe subsets.

Risk: The documented global install command is unpinned for a security-critical wallet CLI.

Mitigation: Install cocod from an authoritative source, pin and verify version 0.0.15, and avoid elevated installs unless required by the environment.

## Reference(s):

- [Cocod ClawHub Skill Page](https://clawhub.ai/egge21m/skills/cocod)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cocod CLI version 0.0.15 and user approval before commands that can spend wallet funds.]

## Skill Version(s):

0.0.15 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
