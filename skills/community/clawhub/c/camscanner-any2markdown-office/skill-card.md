## Description:

Converts PDF and image documents to Markdown using CamScanner's document parsing service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to turn user-selected PDFs and images into Markdown for downstream reading, extraction, and document understanding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are uploaded to CamScanner's servers for processing.

Mitigation: Use the skill only for documents whose upload and stated retention behavior are acceptable; avoid highly confidential, regulated, or third-party-sensitive files unless approved.

Risk: The workflow depends on external API availability and correct file-type handling.

Mitigation: Check each upload, conversion, and download response before using the Markdown output.

## Reference(s):

- [CamScanner Homepage](https://www.camscanner.com)
- [CamScanner AI Tools API](https://ai-tools.camscanner.com)
- [ClawHub Skill Page](https://clawhub.ai/camscanner-ai/skills/camscanner-any2markdown-office)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and downloaded .md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; uploads selected PDF or image files to CamScanner and downloads Markdown output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
