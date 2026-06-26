## Description: <br>
中文OCR双引擎 — PaddleOCR(主力文档OCR) + RapidOCR(手写体特化)，按需灵活切换 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-automation teams use this skill to run Chinese OCR workflows for scanned PDFs, printed documents, handwritten dates, signatures, employee IDs, and batch extraction tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR source PDFs and derived outputs can contain sensitive document data. <br>
Mitigation: Run in a trusted local environment, preferably a virtualenv, and handle generated PDFs, annotations, text files, logs, training data, and temporary images as sensitive when source PDFs are sensitive. <br>
Risk: README examples and installed OCR engines may differ from the available script interfaces or local environment. <br>
Mitigation: Verify each script's --help output and installed dependencies before relying on documented engine examples. <br>
Risk: Broad process-kill commands used for OCR cleanup can stop unrelated Python work. <br>
Mitigation: Use process cleanup only after confirming the target process belongs to the intended OCR task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meta-evo-creator/chinese-handwriting-ocr) <br>
- [OCR tips](references/ocr_tips.md) <br>
- [Lessons learned](references/lessons.md) <br>
- [Tesseract installation reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus local OCR outputs such as text, JSON, annotated PDFs, training data, and model artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and may create temporary images, logs, OCR text, annotations, generated PDFs, training datasets, and model checkpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
