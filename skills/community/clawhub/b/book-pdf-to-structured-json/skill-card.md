## Description:

Convert whole-book PDF, scanned PDF, DOCX, or TXT sources into a publication-grade hierarchical electronic edition with authoritative printed-TOC reconstruction, reviewed OCR cleanup, per-chapter TXT, combined TXT, structured JSON/TSV, deterministic validation, safe API upload, backup, and full read-back verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yasmineliu](https://clawhub.ai/user/yasmineliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to convert complete book sources into reviewed hierarchical JSON/TXT/TSV editions with deterministic validation and optional remote read-back verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A filename validation flaw may allow output files to be written outside the selected output folder.

Mitigation: Review before installing; use only simple book IDs made from letters, numbers, dots, underscores, or hyphens, and write to a dedicated versioned output folder.

Risk: Remote upload or replacement can mutate an external environment if performed without clear authorization and backup evidence.

Mitigation: Perform upload or replacement only after the target environment, backup, credential handling, and read-back export are explicitly approved.

Risk: Automatically generated TOC or OCR output can remain a draft and may not be publication-grade until reviewed.

Mitigation: Treat pending TOC or OCR review as unfinished, require reviewer decisions for OCR candidates, rebuild derivatives, and run strict validation before delivery.

## Reference(s):

- [Pipeline Reference](references/pipeline.md)
- [ClawHub Skill Page](https://clawhub.ai/yasmineliu/skills/book-pdf-to-structured-json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, TSV, TXT, logs, and checksum reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local book-conversion artifacts and validation reports; remote upload guidance is conditional on explicit user authorization.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
