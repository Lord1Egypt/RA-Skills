## Description:

Formats Chinese official documents from DOCX, DOC, WPS, TXT, and Markdown files and produces standardized DOCX output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwyalpha](https://clawhub.ai/user/cwyalpha)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing Chinese official documents can use this agent to standardize document layout, heading levels, typography, page settings, attachments, and batch conversions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill may automatically accept tracked edits beyond formatting, which could change document content.

Mitigation: Review tracked changes and compare the formatted copy with the source before relying on its content.

Risk: The security summary flags opening untrusted legacy documents without disabling macros.

Mitigation: Only process legacy documents from trusted sources, and disable macros when opening them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cwyalpha/skills/doc-format)
- [CLI Reference](artifact/references/cli-reference.md)
- [Config Reference](artifact/references/config-reference.md)
- [Formatting Rules](artifact/references/formatting-rules.md)

## Skill Output:

**Output Type(s):** [Files, Guidance, Configuration instructions]

**Output Format:** [DOCX documents, with Markdown or shell-command guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes formatted copies; supports single files and recursive batch processing, with configurable formatting and output locations.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
