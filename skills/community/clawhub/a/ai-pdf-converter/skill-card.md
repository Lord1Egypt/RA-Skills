## Description:

AI PDF Converter helps agents convert PDFs to Markdown, HTML, LaTeX, DOCX, or JSON using the MinerU API and mineru-open-api CLI with layout analysis, table recognition, formula detection, and OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to guide PDF conversion workflows for scanned documents, academic papers, reports, contracts, and multilingual documents. It selects MinerU CLI commands for quick Markdown extraction, multi-format conversion, AI-enhanced layout handling, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unpinned global third-party CLI.

Mitigation: Review and pin the mineru-open-api version where possible, install it locally or in a sandbox, and scan it before use.

Risk: PDF contents may be processed through MinerU without artifact-level privacy or retention guidance.

Mitigation: Avoid confidential, legal, financial, medical, or proprietary PDFs unless MinerU data-handling terms and required approvals are confirmed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and file-format guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can direct generation of Markdown, HTML, LaTeX, DOCX, or JSON files through mineru-open-api.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
