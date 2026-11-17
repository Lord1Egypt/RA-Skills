## Description:

Ask Miles (askmiles.ai) card and points questions against the owner's real wallet: which card to get next, keep-or-cancel math, transfer partners and ratios, award strategy, and which card to use for a purchase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assareh](https://clawhub.ai/user/assareh)

### License/Terms of Use:

MIT-0

## Use Case:

Cardholders and their personal agents use this skill to compare rewards cards, evaluate keep-or-cancel decisions, plan transfers or awards, and choose a card for a purchase using the account owner's Miles wallet and current catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Granting OAuth access connects the agent to one person's Miles account and usage allowance.

Mitigation: Review the requested OAuth consent and scope before approving, and route only the account owner's questions through that connection.

Risk: The security scan was partial because two local references could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved references and the skill before installing or relying on it.

## Reference(s):

- [Ask Miles](https://askmiles.ai/openclaw?utm_source=skill&utm_medium=assistant)
- [Ask Miles skill source](https://askmiles.ai/skills/ask-miles.md)
- [ClawHub release](https://clawhub.ai/assareh/skills/ask-miles)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only answers about the account owner's wallet and Miles catalog; claims can be qualified using Miles' reported tool provenance.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
