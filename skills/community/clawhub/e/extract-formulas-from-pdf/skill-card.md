## Description:

Extracts mathematical formulas and equations from PDF documents using MinerU, converting native or OCR-recognized math into Markdown with inline LaTeX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical document workflows use this skill to extract equations from PDF papers, textbooks, or document URLs and reuse them as LaTeX-bearing Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs and URLs may be sent to MinerU/OpenDataLab services during extraction.

Mitigation: Use only documents approved for external processing, and avoid confidential or internal-only files unless that service use is authorized.

Risk: The skill installs and runs an unpinned third-party CLI package.

Mitigation: Pin mineru-open-api to a reviewed version and run it in a least-privileged environment.

Risk: Formula extraction requires authentication through MINERU_TOKEN or the mineru-open-api auth flow.

Mitigation: Store tokens in approved secret handling mechanisms and avoid committing credentials to skill files, logs, or generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/extract-formulas-from-pdf)
- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and LaTeX output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mineru-open-api CLI and a MINERU_TOKEN for extraction.]

## Skill Version(s):

0.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
