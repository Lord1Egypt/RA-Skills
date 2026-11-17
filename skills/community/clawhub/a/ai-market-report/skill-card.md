## Description:

Generates daily market research reports for AI companion software by collecting App Store and web research data, then producing Markdown, HTML, and PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vae2024](https://clawhub.ai/user/vae2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect current AI companion app market data and generate structured Chinese-language market reports. It is intended for recurring competitor research that combines App Store metrics, web research, and report rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External research workflows send market queries and retrieved URLs to third-party services.

Mitigation: Use approved services and credentials only, and review data-sharing requirements before running the skill in regulated or confidential contexts.

Risk: Report data gathered from web sources can be incorrect, stale, or unavailable.

Mitigation: Verify cited sources before business use and preserve the skill's rule to mark unavailable metrics as unpublished instead of inventing values.

Risk: Web-derived report content is rendered into HTML and PDF.

Mitigation: Escape or sanitize all report fields and restrict WeasyPrint resource fetching before using the renderer with untrusted content.

Risk: Generated Markdown, HTML, and PDF reports are written to fixed workspace paths.

Mitigation: Run in an isolated workspace or configure controlled output paths, then review and clean generated artifacts after use.

## Reference(s):

- [AI companion data collection guide](references/data_collection.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report plus rendered HTML and PDF files, with shell commands for data collection and report generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped report artifacts to fixed OpenClaw workspace paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
