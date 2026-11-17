## Description:

Generate a professional PDF report from a GEO audit using pandoc + Chrome headless.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO teams, and client-facing analysts use this skill to convert a GEO-AUDIT-REPORT.md file into a styled, client-ready GEO audit PDF with cover metadata, score tables, severity callouts, and roadmap sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow processes local GEO-AUDIT-REPORT.md content through shell and browser-based PDF generation, which can be unsafe for reports from untrusted parties.

Mitigation: Use trusted report inputs, restrict embedded resources, and run the conversion in a constrained working directory.

Risk: The documented Chrome command includes --no-sandbox, reducing browser isolation during local rendering.

Mitigation: Remove --no-sandbox where possible or run the browser step inside an isolated environment.

Risk: Report metadata and output names can affect shell commands and generated files.

Mitigation: Validate or escape metadata before passing it to commands and choose output names deliberately to avoid overwriting existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-report-pdf)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions with bash commands; generated HTML and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GEO-REPORT.html and GEO-REPORT.pdf from GEO-AUDIT-REPORT.md when the required local browser tooling is available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
