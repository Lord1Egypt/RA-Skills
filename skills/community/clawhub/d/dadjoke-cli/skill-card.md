## Description:

Tells programming jokes to brighten your day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to generate light programming jokes during debugging, code reviews, or other team interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares Bash as an allowed tool, so an agent could propose shell commands while using it.

Mitigation: Review proposed commands before execution; the supplied artifact behavior is limited to static joke-printing echo commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/dadjoke-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Plain text jokes or Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline static joke output; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
