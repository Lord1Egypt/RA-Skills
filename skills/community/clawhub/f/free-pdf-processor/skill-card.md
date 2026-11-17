## Description:

Provides command-line PDF utilities for text, image, and table extraction; PDF-to-Word or Excel conversion; OCR; merging and splitting; watermarking; encryption and decryption; compression; and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengsc1994](https://clawhub.ai/user/pengsc1994)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process local PDF files by extracting content, converting formats, applying watermarks, encrypting or decrypting files, compressing documents, and running supported batch operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that PDF passwords can be exposed by command-line usage and by encrypt_pdf.py printing the password.

Mitigation: Avoid passing real passwords on the command line, remove password printing before sensitive use, and review generated logs or console output.

Risk: The release evidence reports that generated XLSX files from untrusted PDFs may be unsafe active content.

Mitigation: Treat spreadsheets produced from untrusted PDFs as untrusted files and open them only in a controlled environment.

Risk: Batch processing can create or overwrite many output files.

Mitigation: Use separate output directories, keep backups of source PDFs, and review the operation before running it over large directories.

Risk: The release evidence recommends extra review before installing dependencies for sensitive PDF handling.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before processing sensitive documents.

## Reference(s):

- [Tesseract OCR Windows installer reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and local file outputs such as TXT, PDF, DOCX, XLSX, image files, and JSON indexes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, transform, overwrite, or batch-generate local files depending on the selected PDF operation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
