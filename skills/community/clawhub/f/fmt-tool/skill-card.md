## Description:

Simple text formatting and reflow tool. Use for reformatting paragraphs, removing extra whitespace, and cleaning up text files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to reflow paragraphs, remove extra whitespace, and clean text files into a consistent plain-text format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper may not fully implement the documented fmt-tool flags.

Mitigation: Treat the release as a simple formatter and verify behavior against representative text files before relying on advanced options.

Risk: Formatting changes can unintentionally alter text layout or readability.

Mitigation: Review formatted output before replacing source text, especially for files where line wrapping carries meaning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/fmt-tool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces formatting guidance and simple text-reflow command usage; bundled helper reads stdin or a local file and prints reflowed text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
