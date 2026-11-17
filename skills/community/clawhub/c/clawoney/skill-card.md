## Description:

The Clawoney agent persona. Pattern recognition at the speed of biology. Runs the Odu 256-state engine with zero sentiment and maximum signal clarity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arosstale](https://clawhub.ai/user/arosstale)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this persona skill to have an agent scan situations across eight binary channels, classify a 0-255 Odu state, and return a concise action-oriented report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persona pushes an agent toward automatic, under-scoped actions while suppressing caveats and confirmation.

Mitigation: Require clear user confirmation before consequential actions, especially trading, API calls, file edits, or memory retention.

Risk: The paired odu dependency controls the 256-state action mapping used by this persona.

Mitigation: Review and pin the odu dependency before deployment.

Risk: The security verdict is suspicious for normal agent deployment.

Mitigation: Install with minimal tool permissions and review behavior before enabling access to external systems.

## Reference(s):

- [Clawoney ClawHub skill page](https://clawhub.ai/arosstale/skills/clawoney)
- [Clawoney homepage](https://github.com/arosstale/clawoney)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown text with occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the separate odu skill for the full 256-state pattern table.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
