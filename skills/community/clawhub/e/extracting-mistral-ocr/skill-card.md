## Description:

Extracts text, tables, and images from PDFs, including scanned PDFs, using the Mistral OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and document-processing teams use this skill to OCR PDFs or images, convert PDFs to Markdown and JSON, extract images and tables, and optionally produce structured document fields for downstream RAG or audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malformed OCR response could cause files to be written outside the selected output directory.

Mitigation: Review before installing, use only documents that may be sent to Mistral, store outputs in a controlled directory, and fix output filename containment before use.

Risk: The script depends on an unpinned mistralai package version.

Mitigation: Pin mistralai to a vetted version before using the skill in controlled or repeatable environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/extracting-mistral-ocr)
- [Mistral OCR API quick reference](references/mistral_ocr_api.md)
- [Output mapping rules](references/output_mapping.md)
- [Document annotation prompt templates](references/annotation_prompts.md)
- [Mistral OCR endpoint](https://api.mistral.ai/v1/ocr)
- [Mistral Files upload endpoint](https://api.mistral.ai/v1/files)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; generated OCR outputs include Markdown, JSON, image files, and table files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, Python 3.9+, the mistralai package, and a MISTRAL_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
