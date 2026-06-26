## Description: <br>
Processes PDF, DOCX, and XLSX supply chain document packages for conversion, image extraction, OCR-assisted review, dimension verification, and summary report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiejingke](https://clawhub.ai/user/jiejingke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quality engineers, and supply chain reviewers use this skill to organize supplier document packages, extract reviewable images and OCR text, check dimension judgement consistency, and generate manual review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR fallback may automatically run an unpinned OCR script found in broad local skill directories. <br>
Mitigation: Prefer HTTP-only OCR or set HERDSMAN_SKILL_DIR to a specific trusted OCR skill before using OCR features. <br>
Risk: Images from the selected task folder may be sent to the configured OCR endpoint. <br>
Mitigation: Use the skill only with task folders intended for processing and configure a trusted OCR endpoint for sensitive documents. <br>
Risk: Seal, stamp, and signature OCR hits can be mistaken for authenticity conclusions. <br>
Mitigation: Treat OCR hits as review clues only and require manual judgement for final authenticity or compliance decisions. <br>


## Reference(s): <br>
- [Environment Setup Guide](references/setup-guide.md) <br>
- [Naming & Directory Conventions](references/naming-conventions.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiejingke/auto-dimension-report-skill-en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, OCR markdown files, converted document files, extracted image files, Excel indexes, optional JSON summaries, and agent-facing shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates output/, image/, imagetomd/, _ImageIndex.xlsx, and ReviewReport.md in the user-provided task folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
