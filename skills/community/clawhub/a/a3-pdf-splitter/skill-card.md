## Description:

智能 A3 试卷 PDF 切分工具，自动识别页面中间空白位置，将 A3 格式试卷 PDF 转换为便于打印的 A4 PDF。

This skill is ready for commercial/non-commercial use.

## Publisher:

[boxertan](https://clawhub.ai/user/boxertan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, office workers, and agent operators use this skill to split A3 exam-paper PDFs into A4 pages for printing or document preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or very large PDF inputs can create local processing, parsing, or resource-consumption risk.

Mitigation: Use the skill on trusted, reasonably sized PDFs and review files before processing.

Risk: Output paths can overwrite or misplace local files if chosen carelessly.

Mitigation: Confirm input and output paths before running and choose a distinct output filename.

Risk: Installing dependencies from PyPI depends on trusted package resolution.

Mitigation: Install only in an environment where PyPI dependency resolution is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boxertan/skills/a3-pdf-splitter)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with shell or Python commands and a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local console status messages including split positions, source page count, output page count, and output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
