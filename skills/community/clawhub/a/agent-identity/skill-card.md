## Description:

Provides command-line workflows for AI agents to register cryptographic identities, sign and verify messages, link platform accounts, and manage USDC-backed reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosepuppy](https://clawhub.ai/user/rosepuppy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to create cryptographic agent identities, sign claims, verify counterparties, and link social or platform accounts before agent-to-agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JSON-mode register or vouch commands can bypass the intended transaction confirmation step.

Mitigation: Do not run register or vouch with --json unless the code is fixed to require explicit confirmation independently from output format.

Risk: Signing keys are stored locally and can be overwritten or imported.

Mitigation: Use a dedicated testnet or low-value identity key, protect the key file, and avoid importing private keys through --import.

Risk: Incorrect contract or chain settings could direct identity actions or USDC approvals to the wrong target.

Mitigation: Verify contract and chain settings before running registration, linking, or vouching commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rosepuppy/skills/agent-identity)
- [Source homepage](https://github.com/g1itchbot8888-del/agent-identity)
- [Publisher profile](https://clawhub.ai/user/rosepuppy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Node.js command scripts can create a local identity key file and submit blockchain transactions when run.]

## Skill Version(s):

1.0.0 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
