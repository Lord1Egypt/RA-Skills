## Description:

ArifOS Sense provides a constitutional governance layer that helps an agent decide when to proceed, warn, pause for human review, or refuse consequential actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariffazil](https://clawhub.ai/user/ariffazil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill to add a decision checkpoint for irreversible, high-stakes, externally consequential, or identity-affecting requests. It produces a verdict and concise reasoning so the agent can proceed, warn, pause for approval, or decline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly pause or block agent actions based on its governance rules.

Mitigation: Review or modify activation conditions before deployment so authority belongs to the authenticated user and use of the governance layer is explicit.

Risk: The skill describes persistent cross-session decision logs with unclear user control.

Mitigation: Make memory logging opt-in, scoped, redactable, and deletable before using it outside the original arifOS workflow.

## Reference(s):

- [The 13 Constitutional Floors](references/floors.md)
- [VAULT999 Audit Ledger Format](references/vault999-format.md)
- [ClawHub skill page](https://clawhub.ai/ariffazil/skills/arifos-sense)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown verdict block with concise reasoning and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to pause for human approval or record a consequential decision in an audit ledger.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
