## Description: <br>
Parses local DOCX and PDF files into report-first knowledge artifacts, including ingest reports, JSONL extraction records, failure logs, and memory candidate drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiasdobi](https://clawhub.ai/user/kaiasdobi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to process locally available DOCX and PDF documents into reviewable knowledge ingestion outputs without directly writing persistent memory. It is suited for batch extraction workflows where failed files, confidence notes, and source references must remain visible for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local summaries, filenames, file paths, and parse-error details are written to generated output files. <br>
Mitigation: Run the skill only on documents you are authorized to process, use a narrow input folder, and review or delete generated outputs after use. <br>
Risk: DOCX and PDF parsing dependencies process local document content and may need updates before handling untrusted files. <br>
Mitigation: Pin and update safe versions of python-docx and pypdf, and process untrusted documents in a constrained environment. <br>
Risk: Scanned PDFs or unsupported file types may produce empty extraction results or failure records. <br>
Mitigation: Review failed-items.jsonl and ingest-report.md, then retry with OCR or inspect the file manually when needed. <br>


## Reference(s): <br>
- [Output examples](artifact/references/output_examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/kaiasdobi/docx-pdf-knowledge-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSONL files, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSONL files, with a small JSON command summary from the local runner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ingest-report.md, kb-items.jsonl, failed-items.jsonl, and MEMORY.candidate.md; does not write MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
