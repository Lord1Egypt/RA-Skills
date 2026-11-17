## Description:

Helps agents make conservative, task-focused edits to existing codebases while preserving architecture, style, and shared-code boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[addxing](https://clawhub.ai/user/addxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to keep agent-assisted code changes narrowly scoped, preserve existing project conventions, and require confirmation before broad architecture or shared-code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may slow broad refactors or shared-code changes by requiring explicit confirmation.

Mitigation: State the intended scope up front and approve architecture, shared-code, or core behavior changes before the agent proceeds.

Risk: A conservative edit posture can preserve flawed existing patterns when a deeper redesign is actually needed.

Mitigation: Pair use with review and testing, and explicitly override the conservative posture when the task requires redesign or cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/addxing/skills/conservative-code-edits)
- [Server-resolved GitHub provenance](https://github.com/addxing/conservative-code-edits)
- [Publisher profile](https://clawhub.ai/user/addxing)

## Skill Output:

**Output Type(s):** [guidance, text, code]

**Output Format:** [Markdown guidance and code-editing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for confirmation before broader refactors, shared-code edits, or architectural changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
