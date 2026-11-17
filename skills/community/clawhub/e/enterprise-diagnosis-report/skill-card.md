## Description:

Consolidates enterprise profile, finance and tax diagnosis, and policy matching reports into a comprehensive enterprise diagnosis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangl271](https://clawhub.ai/user/wangl271)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to parse trusted enterprise diagnosis PDFs, extract company, financial, tax, and policy data, cross-check shared fields, and generate an integrated Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF parser can fetch arbitrary URLs and write extracted content to caller-chosen paths.

Mitigation: Use trusted local PDFs or trusted HTTPS report sources only, avoid attacker-supplied URLs, and keep outputs in a dedicated workspace directory.

Risk: Generated text files may contain sensitive enterprise financial and tax data.

Mitigation: Treat generated reports and extracted text as sensitive and restrict access according to the organization's data handling requirements.

Risk: PDF extraction can misread tables, numbers, scanned pages, or time-sensitive policy details.

Mitigation: Manually verify key figures and policy information before using the report for decisions.

## Reference(s):

- [Report template](references/report_template.md)
- [ClawHub skill page](https://clawhub.ai/wangl271/skills/enterprise-diagnosis-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with extracted PDF text files when an output path is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can mark missing or conflicting report data for user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
