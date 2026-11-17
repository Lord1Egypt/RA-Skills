## Description:

Converts Markdown into formatted Word, HTML, PDF, and presentation files, with optional Omni Reader data for page anchors and source tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use it to turn Markdown or Omni Reader parsing results into formatted, editable Word documents, shareable HTML or PDF, and presentation decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML containing external image links may cause network requests when viewed or printed.

Mitigation: Review image links and use trusted or local images; check browser network behavior before exporting to PDF.

Risk: Installation guidance refers to upstream content without a pinned version.

Mitigation: Review and pin the installation source before installing.

Risk: The security scan is partial and reports reliability and disclosure concerns, leaving incomplete evidence.

Mitigation: Review the reported output-validation limitations and validate results with nonsensitive documents before using sensitive material.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-omni2docx)
- [Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [Omni Reader API key guidance](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Word documents, HTML documents, PDF documents, PowerPoint presentations, Guidance]

**Output Format:** [Word (.docx), HTML, PDF, and PowerPoint (.pptx) files, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatting profiles and optional page marks or source-tracing annotations when Omni Reader data is supplied.]

## Skill Version(s):

0.6.20 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
