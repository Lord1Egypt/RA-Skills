## Description:

For novel, fiddly, or infrastructure-sensitive work, search prior notes and solved cases for a structurally similar problem. Reuse the method as a hypothesis, verify it against current state, test the real outcome falsifiably, and record only the reusable delta.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to check prior notes, logs, scripts, and solved cases before tackling unfamiliar or drift-sensitive work. It helps adapt previous methods as hypotheses, verify them against current state, and record only reusable deltas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to search broad memory, notes, scripts, wikis, or conversation history that can contain sensitive or unrelated private material.

Mitigation: Use scoped, user-approved knowledge stores and avoid searching locations likely to contain credentials or unrelated private content.

Risk: Retrieved prior notes can be stale, incomplete, or misleading for the current task.

Mitigation: Treat prior solutions only as hypotheses, inspect current state before changes, and verify the user-relevant outcome with a falsifiable test.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/pinguy/Skills/tree/main/skills/check-notes-first)
- [ClawHub skill page](https://clawhub.ai/pinguy/skills/check-notes-first)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional inline commands and structured notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed output schema; the skill guides retrieval, comparison, verification, and compact note updates.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
