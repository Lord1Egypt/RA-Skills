## Description:

Encodes and decodes text or URLs to handle Chinese characters, spaces, and special characters in URL-safe form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lapidcj](https://clawhub.ai/user/lapidcj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to locally encode text or URLs into percent-encoded form and decode percent-encoded strings back into readable text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous input may be auto-encoded or auto-decoded incorrectly.

Mitigation: Ask for an explicit encode or decode action when the intended operation is unclear, or show both results for user review.

Risk: Users who do not prefer Chinese may receive responses that are less accessible.

Mitigation: Ask the agent to respond in the user's preferred language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lapidcj/skills/cj-url-encoder)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with original text, encoded or decoded result, and a brief explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing with no external dependencies; output may include status or error messaging.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
