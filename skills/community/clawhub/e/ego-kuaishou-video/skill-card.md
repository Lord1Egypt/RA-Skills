## Description:

Publish a local video to the Kuaishou creator platform with Ego Lite after checking login, with optional creator-backend comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill to submit a caller-provided local video and description to the Kuaishou creator platform, or optionally post a comment on a selected work. It checks login first and reports whether the work reached review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing and commenting submit content directly through the creator account and may target unintended account, video, text, or visibility settings.

Mitigation: Confirm the creator account, video, text, and visibility before invoking; provide a title hint for comments.

Risk: Concurrent runs share fixed temporary filenames, and leftover configuration files or screenshots may contain sensitive information.

Mitigation: Avoid simultaneous runs and remove leftover configs or screenshots when sensitive.

## Reference(s):

- [Kuaishou Creator Platform](https://cp.kuaishou.com)
- [Input requirements](artifact/references/inputs.md)
- [Login guidance](artifact/references/login.md)
- [Kuaishou publishing and commenting pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Shell command invocations and JSON status messages with concise user guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a caller-provided local video file and description; commenting is optional and can use a title hint to identify the work.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
