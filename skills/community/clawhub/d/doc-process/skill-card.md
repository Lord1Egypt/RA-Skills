## Description:

Doc Process helps agents classify documents, autofill forms, analyze contracts, receipts, bank statements, resumes, IDs, medical records, meetings, tables, translations, redactions, and document scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piyush-zinc](https://clawhub.ai/user/piyush-zinc)

### License/Terms of Use:


## Use Case:

Developers and document-heavy users use this skill to route document requests into focused workflows for extraction, review, redaction, summarization, translation, transcription, and scan cleanup. It can produce human-readable analysis and optional local file outputs through bundled scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install unpinned packages, change system packages, and run a remote pip bootstrap.

Mitigation: Review setup.sh before installation, prefer a virtual environment, install only the dependency group needed, and avoid approving sudo or remote bootstrap execution unless those host changes are acceptable.

Risk: Document workflows may involve sensitive personal, financial, medical, legal, or identity data.

Mitigation: Keep timeline logging off for sensitive documents or use sanitized filenames and category-only summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/piyush-zinc/skills/doc-process)
- [Bank Statement Analyzer Reference Guide](references/bank-statement-analyzer.md)
- [Contract Analyzer Reference Guide](references/contract-analyzer.md)
- [Doc Scan Reference Guide](references/doc-scan.md)
- [Document Categorizer Reference Guide](references/document-categorizer.md)
- [Document Timeline Reference Guide](references/document-timeline.md)
- [Document Translator Reference Guide](references/document-translator.md)
- [Form Autofill Reference Guide](references/form-autofill.md)
- [ID & Passport Scanner Reference Guide](references/id-scanner.md)
- [Legal Document Redactor Reference Guide](references/legal-redactor.md)
- [Medical Document Summarizer Reference Guide](references/medical-summarizer.md)
- [Meeting Minutes Extractor Reference Guide](references/meeting-minutes.md)
- [Receipt Scanner Reference Guide](references/receipt-scanner.md)
- [Resume / CV Parser Reference Guide](references/resume-parser.md)
- [Table & Data Extractor Reference Guide](references/table-extractor.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with tables, inline shell commands, and optional CSV, JSON, text, PDF, or image file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some script-assisted modes require local Python packages or system binaries; audio transcription may download a Whisper model on first use.]

## Skill Version(s):

4.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
