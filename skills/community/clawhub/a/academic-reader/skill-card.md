## Description:

PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local PDFs or PDF URLs into Markdown for extraction, summarization, parsing, and analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDFs or PDF URLs are sent to MinerU for processing.

Mitigation: Confirm before uploading sensitive documents and use this skill only when third-party processing is acceptable.

Risk: The skill depends on installing and running the mineru-open-api CLI.

Mitigation: Prefer a reviewed pinned CLI version or verified artifact for stronger supply-chain control.

Risk: The larger authenticated extraction workflow changes the data-handling posture.

Mitigation: Avoid `mineru-open-api auth` unless the authenticated workflow is required and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanis90/skills/academic-reader)
- [MinerU homepage](https://mineru.net)
- [MinerU CLI download page](https://mineru.net/ecosystem?tab=cli)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns Markdown from selected local PDFs or PDF URLs and supports page ranges and language hints; no-auth extraction is documented as limited to 10MB or 20 pages.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
