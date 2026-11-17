## Description:

Use when the user wants to review auto-memory, promote durable instructions into CLAUDE.md or local memory, and clean up duplicates or conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to audit project, local, and auto-memory layers, identify durable memory candidates, and surface duplicate, stale, or conflicting instructions before approving changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect memory-related content that includes private preferences or project instructions.

Mitigation: Use it only when that review is intended, and ask the agent to list memory locations first if tighter control is needed.

Risk: Incorrect memory promotions or cleanup could preserve misleading guidance or remove useful context.

Mitigation: Review the grouped report and approve specific changes before any edits are applied.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with proposed promotions, cleanup findings, and no-change recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents proposals before edits and requires explicit approval before applying promotions or cleanup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
