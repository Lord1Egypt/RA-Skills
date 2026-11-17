## Description:

Doc Genius helps agents summarize PDF, Word, Markdown, and text documents, convert documents to Markdown or HTML, and run batch document processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:


## Use Case:

Developers, researchers, content teams, and enterprise users can use this skill to summarize documents, convert common document formats, and process folders of files into structured summaries or converted outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive document content can be sent to an external AI provider when AI or auto summarization uses a configured API key.

Mitigation: Use local or TextRank mode for sensitive documents, and select AI or auto mode only when remote processing is intended and approved.

Risk: The paid processor includes under-disclosed billing behavior and an embedded billing credential.

Mitigation: Do not run the paid processor until billing behavior is documented and the embedded credential is removed and rotated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imgolye/skills/doc-genius)
- [API Examples](references/api-examples.md)
- [Supported Formats](references/supported-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, plain text, HTML, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write converted document files or batch report files when an output path or report path is provided.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
