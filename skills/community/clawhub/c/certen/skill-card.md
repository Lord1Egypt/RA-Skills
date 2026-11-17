## Description:

Give this agent a CERTEN identity and let it execute proof-gated actions on any chain it is linked to. It never spends without the owner's explicit consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-gregoire](https://clawhub.ai/user/jason-gregoire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to give an agent a CERTEN on-chain identity, execute owner-approved proof-gated actions, and share verifiable receipts for high-trust workflows such as escrow, settlement, arbitration, insurance, and regulated approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through on-chain actions that may move owner funds or trigger governance-sensitive operations.

Mitigation: Require explicit per-action owner approval after showing quote and balance details, and do not proceed on silence.

Risk: CERTEN signing and API credentials are created and persisted outside the skill, and mishandling them could expose signing access.

Mitigation: Use a dedicated testnet identity first, avoid storing credentials in shared or committed workspaces, and prefer encrypted or access-controlled secret storage.

Risk: The installed CERTEN CLI performs the operational actions described by the skill.

Mitigation: Pin and review the CERTEN CLI version before deployment.

## Reference(s):

- [CERTEN Skill Page](https://clawhub.ai/jason-gregoire/skills/certen)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the CERTEN CLI and generally support --json responses wrapped with ok, data, and error fields.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
