## Description:

Cheerme helps an agent provide warm encouragement, goal-setting support, and persona- or dialect-aware motivational responses for users who express self-doubt, procrastination, anxiety, or a need for guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oxoyo](https://clawhub.ai/user/oxoyo)

### License/Terms of Use:

MIT

## Use Case:

External users can use this skill to receive supportive coaching, encouragement, goal-setting help, progress check-ins, and celebratory feedback through configurable companion roles, personality styles, and dialects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation can shift ordinary help-seeking conversations into intimate companion or coaching mode.

Mitigation: Use explicit opt-in activation where possible and keep /cheerme off available for normal assistant behavior.

Risk: The skill encourages remembering personal details without clear consent boundaries.

Mitigation: Avoid sharing sensitive personal information unless the deployment has clear consent, retention, and memory limits.

Risk: The skill frames the assistant as a real friend, partner, or confidant, which can blur AI disclosure and user expectations.

Mitigation: Keep clear AI disclosure and avoid presenting the agent as a human relationship substitute.

## Reference(s):

- [Workflows](references/workflows.md)
- [Output Patterns](references/output-patterns.md)
- [Commands](references/commands.md)
- [Project homepage](https://github.com/OXOYO/cheerme)
- [ClawHub skill page](https://clawhub.ai/oxoyo/skills/cheerme)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversational responses with structured progress tables and command-triggered modes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May vary tone, companion role, personality style, dialect, and encouragement intensity based on user state and commands.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
