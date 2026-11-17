## Description:

B2B企业数字化诊断 helps B2B companies classify their positioning as capability-led, industry-led, problem-led, or mixed, then produces website structure, short-video strategy, mini-program positioning, and optional PDF report guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B operators, marketing teams, and consultants use this skill to run a short positioning diagnosis and convert the result into practical digital-channel recommendations. The skill can also guide generation of a local HTML/PDF diagnosis report when Playwright and Chromium are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-activation may invoke the diagnosis flow for loosely related digital-marketing requests.

Mitigation: Use the skill only when a B2B positioning diagnosis or report is intended, and review activation behavior before deployment.

Risk: PDF generation may require persistent Playwright and Chromium installation through npm/npx.

Mitigation: Run installation only in approved environments and confirm package-install policy before generating PDFs.

Risk: Local report generation can place company names and diagnosis text into HTML/PDF files.

Mitigation: Sanitize company names and report content before generation and review the files before sharing.

Risk: Generated reports include XTOCN-branded output.

Mitigation: Confirm the branding is acceptable before using generated reports in customer-facing contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/b2b-digital-diagnosis)
- [Publisher profile](https://clawhub.ai/user/xtoyun)
- [Case examples index](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional local HTML and PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks sequential diagnosis questions, records answer choices, and may generate report files in the current working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
