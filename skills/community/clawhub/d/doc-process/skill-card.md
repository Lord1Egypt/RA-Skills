## Description: <br>
Doc Process provides document intelligence for categorization, form autofill, contract and bank statement analysis, receipt and invoice scanning, resume and ID parsing, medical summarization, PII redaction, meeting minutes, table extraction, translation, and document photo cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piyush-zinc](https://clawhub.ai/user/piyush-zinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to route and process documents, extract structured information, summarize or translate content, redact sensitive data, and generate local file outputs when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic setup can install Python packages and system binaries on the host environment. <br>
Mitigation: Review setup.sh and requirements.txt before first use, and avoid automatic setup or sudo package installation unless host changes are acceptable. <br>
Risk: The skill can process sensitive documents such as IDs, bank statements, medical records, and resumes. <br>
Mitigation: Use the skill only on intended documents and limit document access to the pages or files needed for the requested task. <br>
Risk: Timeline or expense logging can write local destination files. <br>
Mitigation: Enable logging only after confirming the exact destination file and the information that will be written. <br>
Risk: Audio transcription may download a Whisper model on first use. <br>
Mitigation: Confirm that the dependency and model download are acceptable before running audio transcription. <br>


## Reference(s): <br>
- [Bank Statement Analyzer Reference Guide](references/bank-statement-analyzer.md) <br>
- [Contract Analyzer Reference Guide](references/contract-analyzer.md) <br>
- [Doc Scan Reference Guide](references/doc-scan.md) <br>
- [Document Categorizer Reference Guide](references/document-categorizer.md) <br>
- [Document Timeline Reference Guide](references/document-timeline.md) <br>
- [Document Translator Reference Guide](references/document-translator.md) <br>
- [Form Autofill Reference Guide](references/form-autofill.md) <br>
- [ID & Passport Scanner Reference Guide](references/id-scanner.md) <br>
- [Legal Document Redactor Reference Guide](references/legal-redactor.md) <br>
- [Medical Document Summarizer Reference Guide](references/medical-summarizer.md) <br>
- [Meeting Minutes Extractor Reference Guide](references/meeting-minutes.md) <br>
- [Receipt Scanner Reference Guide](references/receipt-scanner.md) <br>
- [Resume / CV Parser Reference Guide](references/resume-parser.md) <br>
- [Table & Data Extractor Reference Guide](references/table-extractor.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with tables, JSON, CSV, text, PDF, image file outputs, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some file-output modes write local files and optional setup installs dependencies; audio transcription may download a Whisper model on first use.] <br>

## Skill Version(s): <br>
4.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
