## Description:

Local OCR and chart-recognition skill for extracting Chinese and English text and approximate structured chart data from local images without relying on external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchongyong](https://clawhub.ai/user/chenchongyong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to run local OCR on screenshots, document images, scans, tables, and charts, then save text, TSV, JSON, or debug outputs for review and integration. It is especially relevant when image files should remain local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch OCR can process unintended local files or sensitive screenshots if pointed at a broad directory.

Mitigation: Run batch OCR only on intended directories and redact or exclude sensitive images from evaluation or training folders unless explicitly permitted.

Risk: OCR and chart extraction can be low-confidence or approximate, especially for poor-quality images or heuristic chart parsing.

Mitigation: Use the emitted confidence, quality warning, suggestions, and optional visualization output to decide when to rerun with better parameters or perform human review.

Risk: Unpinned OCR and image-processing dependencies can change behavior or introduce supply-chain risk.

Mitigation: Install dependencies in a virtual environment and prefer pinned, reviewed package versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchongyong/skills/ccy-ocr-local)
- [Skill usage guide](artifact/SKILL.md)
- [Project README](artifact/README.md)
- [OCR configuration guide](artifact/OCR-CONFIG.md)
- [ICDAR 2019 Robust Reading Challenge MLT dataset](https://rrc.cvc.uab.es/?ch=15&com=downloads)
- [ICDAR 2019 Robust Reading Challenge dataset](https://rrc.cvc.uab.es/?ch=14&com=downloads)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and Python snippets; OCR runs may produce plain text, TSV, JSON, manifest files, or optional debug images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode can write per-image outputs and a manifest; JSON output includes confidence and quality guidance for review.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
