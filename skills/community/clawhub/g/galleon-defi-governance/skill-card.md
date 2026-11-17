## Description:

Guides research into DAO proposals and voting power, prepares authorized votes or delegation, and tracks timelock and treasury execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

DAO participants and governance teams use this skill to research proposals, evaluate voting choices and permissions, prepare authorized governance actions, and track execution status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance writes such as votes, delegations, proposals, and treasury execution can create public or financial effects.

Mitigation: Keep research read-only; require separate explicit approval for each public action and verify the exact proposal, choice, actor, permissions, and transaction effects before signing.

Risk: Excess provider access or wallet permissions may grant broader governance authority than the task requires.

Mitigation: Connect only the accounts, API keys, wallet permissions, and Snapshot aliases necessary for the requested work; keep credentials and signed messages out of public artifacts.

Risk: Proposal prose, transaction payloads, and reported execution state may disagree.

Mitigation: Compare executable actions against official proposal sources and reconcile votes, timelock status, and onchain execution before reporting completion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-defi-governance)
- [Provider interfaces](artifact/references/providers.md)
- [Task examples and user configuration](artifact/references/task-examples.md)
- [Governance review and evaluation cases](artifact/references/workflows.md)
- [Snapshot MCP documentation](https://docs.snapshot.box/tools/snapshot-mcp)
- [OpenZeppelin governance documentation](https://docs.openzeppelin.com/contracts/5.x/governance)
- [Safe SDK documentation](https://docs.safe.global/sdk/overview)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown decision brief or action receipt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the proposal, actor, current state, sources, and remaining steps.]

## Skill Version(s):

0.1.3 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
