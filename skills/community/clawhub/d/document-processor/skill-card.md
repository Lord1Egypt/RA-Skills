## Description: <br>
Processes PDF and Word documents with local tools for conversion, page extraction, OCR-assisted analysis, and batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youmu88](https://clawhub.ai/user/youmu88) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and document-processing users use this skill to choose and run local scripts for PDF and Word conversion, PDF page extraction, OCR page analysis, and batch file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can modify the Python environment or require elevated package-management permissions. <br>
Mitigation: Install dependencies in a virtual environment and avoid administrator or root execution. <br>
Risk: Document conversion and extraction can process unintended files or overwrite existing outputs. <br>
Mitigation: Process only explicitly selected files and folders, and use new output filenames for each operation. <br>
Risk: OCR processing can leave temporary files containing sensitive document content. <br>
Mitigation: Delete OCR temporary directories after processing sensitive documents. <br>


## Reference(s): <br>
- [Document Processor ClawHub page](https://clawhub.ai/youmu88/document-processor) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with command-line examples; local outputs may include PDF, DOCX, extracted text, images, and OCR temporary files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python document-processing scripts and may create or overwrite user-selected output files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README changelog, released 2026-03-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
