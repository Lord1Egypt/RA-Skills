## Description:

Helps translate PDFs while preserving page layout, producing bilingual and translation-only PDFs with document triage and batch reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document translators use this skill to triage and translate individual or batched PDFs while retaining figures, formulas, and page layout. It provides an offline direct workflow for suitable born-digital PDFs and an endpoint-backed workflow for other supported documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch mode may follow linked PDFs outside the selected directory and send their text to a translation service.

Mitigation: Do not batch-process directories writable by others or automated systems until symlink containment is fixed; review selected files before running.

Risk: PDF text, OCR text, or seeded terminology may leave the machine through the configured translation endpoint.

Mitigation: Use only endpoints approved for the document's sensitivity; prefer offline direct mode for suitable sensitive PDFs.

Risk: AI-assisted translations and scanned-document OCR may contain errors.

Mitigation: Review translations before formal use; treat tier-C scanned results as preview quality only.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/docsor1212/skills/doc-holmes)
- [Skill homepage](https://skillhub.cn)
- [Engine matrix](references/engine-matrix.md)
- [PDF triage guide](references/triage.md)
- [Batch processing guide](references/batch-iron-rules.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, PDF files, Markdown reports, JSON audit records]

**Output Format:** [Markdown guidance and commands; translated PDFs and audit reports when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual and translation-only PDFs; batch runs include audit logs and reports.]

## Skill Version(s):

3.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
