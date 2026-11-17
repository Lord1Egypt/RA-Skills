## Description:

Count string length deterministically for text with hard limits. Use this skill when a post, reply, caption, commit message, or other text must stay within a maximum character count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evandataforge](https://clawhub.ai/user/evandataforge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to check final text against strict character limits before posting or saving content. It is useful for posts, replies, captions, commit messages, and other text where exact Python string length is an acceptable local gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic invocation may process sensitive draft text when an agent checks content against a character limit.

Mitigation: Confirm when character counting is being performed for sensitive drafts and keep execution local to the bundled script.

Risk: The skill counts Python string length and may not match platform-specific weighting for URLs, Unicode, or special tokens.

Mitigation: Use a platform-specific validation step when exact target-platform enforcement is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evandataforge/skills/character-count)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON or plain text output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Counts exact Python string length, reports chars, limit, remaining, and ok status.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
