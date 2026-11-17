## Description:

Shared medical-document preprocessing utility that loads PDF, Word, spreadsheet, text, JSON, and image files into normalized text, page, JSON, or table artifacts for downstream skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this shared library to preprocess medical documents into consistent intermediate artifacts before downstream extraction, review, or conversion workflows. It is intended for local file parsing and OCR helper use where PHI/PII handling controls remain in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical documents may contain PHI or PII.

Mitigation: Process files only in environments with appropriate data-handling controls and avoid unnecessary exposure of sensitive inputs or extracted artifacts.

Risk: Parsing and OCR depend on local packages and binaries such as openpyxl, pypdf, LibreOffice, pdftotext, and tesseract.

Mitigation: Use trusted local installations, keep them updated, and avoid processing untrusted documents on privileged hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/doc-preprocess)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)

## Skill Output:

**Output Type(s):** [text, json, code, configuration]

**Output Format:** [Python dictionaries containing text, pages, JSON data, or table rows, plus integration guidance and dependency commands in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports txt, md, json, csv, xlsx, xls, docx, doc, pdf, and common image formats; optional dependencies and local binaries are required for some formats.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
