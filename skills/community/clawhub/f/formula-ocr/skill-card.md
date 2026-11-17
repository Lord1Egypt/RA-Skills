## Description:

Formula Ocr helps agents OCR mathematical formulas from PDFs and images using MinerU and return editable LaTeX or text representations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, educators, and developers use this skill to convert equation screenshots, scanned pages, PDFs, and image files into structured LaTeX or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula OCR requires the third-party MinerU CLI/service and may process submitted PDFs or images outside the local agent environment.

Mitigation: Use it only where MinerU processing is approved, and avoid confidential, regulated, or private documents unless external processing has been reviewed.

Risk: The skill requires a MINERU_TOKEN for extraction and crawl operations.

Mitigation: Scope the token to the process that needs it, avoid storing it in shared files, and rotate it according to the user's credential policy.

Risk: Installing mineru-open-api with an unpinned package command can pick up future CLI changes.

Mitigation: Prefer a pinned, reviewed CLI version for controlled deployments.

## Reference(s):

- [Formula Ocr ClawHub page](https://clawhub.ai/mzlzyca/skills/formula-ocr)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance centers on using mineru-open-api; extracted OCR results are produced by the external MinerU CLI/service.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
