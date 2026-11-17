## Description:

Parses local DOCX and PDF files into structured, reviewable knowledge artifacts, including ingest reports, JSONL item files, and memory candidate Markdown without directly writing memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiasdobi](https://clawhub.ai/user/kaiasdobi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to process locally available DOCX and PDF documents into reviewable knowledge-ingestion outputs. It is suited for report-first workflows that require extracted summaries, parse failures, and memory candidates to be inspected before anything is added to persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document summaries and parse errors are written to the selected output directory.

Mitigation: Choose an appropriate output location and review generated files before sharing or importing them into other systems.

Risk: Untrusted or very large DOCX/PDF files can expose parser hardening gaps such as missing size limits, page-count limits, timeouts, and dependency locking.

Mitigation: Run only on trusted, reasonably sized files unless additional size, page-count, timeout, and dependency-locking controls are added.

Risk: Extracted summaries may contain sensitive information from source documents.

Mitigation: Review MEMORY.candidate.md manually and keep sensitive data out of persistent memory unless the workflow explicitly permits it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiasdobi/skills/docx-pdf-knowledge-parser)
- [Output examples](artifact/references/output_examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSONL records, and command-line status JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ingest-report.md, kb-items.jsonl, failed-items.jsonl, and MEMORY.candidate.md in the selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
