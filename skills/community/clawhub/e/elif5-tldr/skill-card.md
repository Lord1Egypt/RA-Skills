## Description:

Forces offering ELI5 or TLDR options after complex responses. Always present simplified alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make assistants offer simplified ELI5 and TLDR follow-ups after longer, technical, or multi-step responses. It is intended to improve accessibility and quick comprehension in conversational answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add ELI5/TLDR option text when an exact machine-readable output is expected.

Mitigation: Avoid using it for strict JSON, code-only, or protocol-bound workflows unless higher-priority instructions explicitly suppress extra response text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tooled-app/skills/elif5-tldr)
- [Publisher profile](https://clawhub.ai/user/tooled-app)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text appended to agent responses with selectable ELI5, TLDR, and Full options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add extra explanatory options after complex responses; exact machine-readable workflows should suppress this behavior with higher-priority instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
