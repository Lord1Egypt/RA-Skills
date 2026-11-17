## Description:

Chinese Handwriting OCR helps agents run PaddleOCR and RapidOCR workflows for Chinese document OCR, handwritten date extraction, batch processing, and OCR model-training support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to extract Chinese text, handwritten dates, signatures, and employee IDs from PDFs, select OCR engines by document type, and run batch OCR or training utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the documentation does not accurately match the actual OCR engines and that documented commands or engine choices may fail or behave differently than advertised.

Mitigation: Review the target scripts and test the selected OCR engine commands in an isolated environment before relying on results in a production document workflow.

Risk: The security guidance says the skill may install mutable ML dependencies and render PDFs to temporary image files.

Mitigation: Pin and review dependencies, run the skill in controlled directories, and clean temporary files after processing sensitive PDFs.

Risk: The security summary says extracted document text can be persisted without clear enough disclosure.

Mitigation: Treat OCR outputs, generated PDFs, annotations, logs, TXT files, JSON results, and training outputs as sensitive derived data and route them through the same retention controls as source documents.

## Reference(s):

- [Chinese Handwriting OCR release page](https://clawhub.ai/meta-evo-creator/skills/chinese-handwriting-ocr)
- [OCR parameters and tips](references/ocr_tips.md)
- [Handwriting OCR lessons learned](references/lessons.md)
- [Tesseract installation reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON-capable OCR output, generated PDF/TXT artifacts, and training data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install OCR and ML dependencies, render PDF pages to temporary images, and write extracted text to PDFs, TXT files, annotations, logs, JSON results, or training outputs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
