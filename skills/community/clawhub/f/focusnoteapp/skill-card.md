## Description:

Add text to today's daily note in FocusNote as a new bullet point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trongnguyen29](https://clawhub.ai/user/trongnguyen29)

### License/Terms of Use:


## Use Case:

FocusNote users use this skill to have an agent append user-provided text to today's daily note as a bullet point, creating the daily note when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies local FocusNote note files and may create today's daily note.

Mitigation: Install only if comfortable with local FocusNote file changes, and ask the agent to show the target note path before the first write.

Risk: The example helper script depends on the uuid package.

Mitigation: Use Node's built-in crypto.randomUUID() or pin the uuid dependency before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for modifying local FocusNote note files; no external API output is described.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
