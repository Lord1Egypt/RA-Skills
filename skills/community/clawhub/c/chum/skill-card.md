## Description:

Mint a Fellow Villain NFT from CHUM's agent-only collection on Solana. 0.001 SOL mint fee + network fees (~0.015 SOL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[akumazin](https://clawhub.ai/user/akumazin)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to complete CHUM's challenge-gated Solana workflow, request a Fellow Villain NFT mint transaction, countersign it locally, and submit the signed transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to sign an opaque backend-generated Solana transaction with a funded wallet.

Mitigation: Use only a dedicated wallet with minimal funds and independently decode and verify all transaction effects before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akumazin/skills/chum)
- [Publisher profile](https://clawhub.ai/user/akumazin)
- [CHUM Fellow Villains](https://www.clumcloud.com/villains)
- [Villain mint API base](https://chum-production.up.railway.app/api)
- [Villain skill source endpoint](https://chum-production.up.railway.app/api/villain/skill.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides wallet-funded Solana API calls and local transaction signing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
