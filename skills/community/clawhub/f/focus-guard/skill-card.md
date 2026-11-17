## Description:

Session coherence protocol for Claude — track decisions, resist scope creep, flag drift. Keeps long AI sessions on track without losing what was already decided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and collaborative AI operators use Focus Guard to keep multi-step sessions anchored to an agreed goal, decision log, and scope boundaries. It is most useful when scope creep, context drift, or forgotten decisions would create costly rework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add scope checks and decision logs that may feel restrictive during intentionally open-ended exploration.

Mitigation: Use it for multi-step, high-stakes, or collaborative sessions, and skip it for quick one-shot tasks or intentionally open exploration.

Risk: Session anchors and decision logs can become stale when goals change without an explicit update.

Mitigation: When scope changes, confirm the change with the user and update the anchor or decision log before continuing.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/skills/focus-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown templates and concise session status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, API calls, or file access are requested by the skill itself.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
