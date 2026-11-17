## Description:

Emotion switch lets users explicitly set a Chinese-oriented assistant's conversational emotional tone and intensity for the current chat until it is changed or reset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npccxx](https://clawhub.ai/user/npccxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an assistant to keep a requested emotional tone, such as happy, sad, angry, calm, excited, lazy, anxious, or playful, during the current conversation. It is useful when a Chinese-language chat experience needs a stable emotional style with adjustable intensity from 1 to 5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent emotional tone can make later neutral, multilingual, or strictly professional tasks feel inappropriate.

Mitigation: Reset or explicitly override the tone before neutral, multilingual, or professional work.

Risk: High-intensity angry or playful tones can make responses feel too sharp for sensitive topics.

Mitigation: Suspend or reduce the emotional tone for safety, serious, or urgent requests, and keep criticism directed at issues rather than the user.

## Reference(s):

- [Emotion guide](references/emotion-guide.md)
- [Emotion intensity examples](references/emotion-intensity-examples.md)
- [ClawHub skill page](https://clawhub.ai/npccxx/skills/emotion-switch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language assistant responses, typically plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains the requested emotional tone only within the current conversation and can be reset or overridden by the user.]

## Skill Version(s):

1.1.3 (source: server release evidence; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
