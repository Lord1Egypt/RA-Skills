## Description: <br>
A one-stop PDF processing skill for extracting text, images, and tables; converting PDFs to Word or Excel; merging, splitting, OCR processing, watermarking, encrypting, decrypting, compressing, and batch processing PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengsc1994](https://clawhub.ai/user/pengsc1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and document-processing users can use this skill to run local PDF utilities for extraction, conversion, OCR, merge/split, watermarking, encryption, decryption, compression, and batch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The encryption script exposes the PDF password in console output. <br>
Mitigation: Remove password printing before using the encryption workflow and prefer a hidden prompt or protected secret source instead of a positional CLI password. <br>
Risk: Document and image parser dependencies are not pinned, increasing supply-chain and parser-risk exposure in shared or automated workflows. <br>
Mitigation: Pin, review, and audit the parser dependencies before processing sensitive or untrusted PDFs. <br>
Risk: The skill processes local PDFs that may contain sensitive content. <br>
Mitigation: Review the skill before installation and use it in a controlled local environment for sensitive documents. <br>


## Reference(s): <br>
- [Tesseract OCR installation guidance](https://github.com/UB-Mannheim/tesseract/wiki) <br>
- [ClawHub skill page](https://clawhub.ai/pengsc1994/free-pdf-processor) <br>
- [Publisher profile](https://clawhub.ai/user/pengsc1994) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; local script outputs may include text, JSON indexes, images, PDF files, DOCX files, and XLSX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local PDF-processing dependencies; OCR also requires a Tesseract installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
