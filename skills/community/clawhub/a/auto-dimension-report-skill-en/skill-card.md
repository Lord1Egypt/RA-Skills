## Description:

Process PDF, DOCX, and XLSX supply chain document packages for conversion, image extraction, OCR-assisted clue review, dimension judgement verification, and review report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiejingke](https://clawhub.ai/user/jiejingke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and quality reviewers use this skill to organize supplier document packages, extract traceable images and OCR text, check dimension table judgements against measured values, and generate a manual review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR can send sensitive document images to a configurable OCR endpoint.

Mitigation: Use a trusted local HERDSMAN_BASE_URL and avoid routing supplier documents to untrusted OCR services.

Risk: The OCR workflow can automatically execute a fallback OCR script found in another skill directory.

Mitigation: Use HTTP-only OCR or set HERDSMAN_SKILL_DIR or ocr_script_dir only to a trusted OCR skill path before enabling script fallback.

Risk: Generated reports and indexes may contain sensitive document text, image paths, and local path information.

Mitigation: Store outputs in controlled task folders and review generated Markdown, XLSX indexes, and OCR files before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiejingke/skills/auto-dimension-report-skill-en)
- [Setup Guide](artifact/references/setup-guide.md)
- [Naming & Directory Conventions](artifact/references/naming-conventions.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated Markdown reports, copied or converted document files, extracted image files, OCR Markdown files, and XLSX indexes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates output/, image/, imagetomd/, output/_ImageIndex.xlsx, and ReviewReport.md in the user-provided task folder when the corresponding workflow steps run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
