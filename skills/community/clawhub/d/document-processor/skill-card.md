## Description:

Document Processor helps agents work with PDF and Word files, including format conversion, page extraction, OCR, watermark handling, merging, splitting, and batch operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youmu88](https://clawhub.ai/user/youmu88)

### License/Terms of Use:

MIT License

## Use Case:

Developers, employees, and external users can use this skill to have an agent prepare document-processing commands and operate local PDF and Word workflows such as conversion, page extraction, OCR-assisted page mapping, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency installer can install or upgrade Python packages from PyPI in the active environment.

Mitigation: Use a virtual environment, review requested packages before installation, and avoid running the installer as administrator or root.

Risk: OCR processing may retain temporary files under /tmp/pdf_ocr_* that can contain document-derived content.

Mitigation: Avoid OCR on confidential documents unless temporary artifacts are manually removed after processing.

Risk: Document operations read from and write to local paths selected by the user.

Mitigation: Keep backups of original files and use explicit output paths to avoid overwriting or misplacing processed documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youmu88/skills/document-processor)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated local document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local Python dependencies and user-selected input and output file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact README changelog, released 2026-03-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
