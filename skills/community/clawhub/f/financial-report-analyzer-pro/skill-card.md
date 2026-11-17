## Description:

Analyzes normalized financial statement data to compute key ratios, identify heuristic red-flag findings, and render JSON or Markdown financial analysis reports.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to run a local financial statement analysis workflow over normalized JSON data, producing ratio calculations, red-flag checks, and report output. It should not be relied on for investment, audit, or business decisions without independent verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package documentation describes broader PDF, XBRL, and Excel analysis capabilities than the bundled runnable pipeline demonstrates.

Mitigation: Treat the release as a normalized-JSON demo unless the claimed ingestion components are separately verified.

Risk: Generated financial analysis may be incomplete or misleading if used as the basis for investment, audit, or business decisions.

Mitigation: Independently check source filings and generated reports before relying on any output.

Risk: Red-flag detections are heuristic signals, not determinations of misconduct or financial condition.

Mitigation: Use red flags as prompts for follow-up review and keep conclusions descriptive.

## Reference(s):

- [Project homepage from ClawHub metadata](https://github.com/openclaw-skills/financial-report-analyzer)
- [Ratio Definitions](artifact/knowledge/ratio_definitions.md)
- [IFRS Standards](https://www.ifrs.org/issued-standards/)
- [FASB Accounting Standards Codification](https://asc.fasb.org/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON or Markdown financial analysis reports with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled pipeline supports normalized financial JSON; non-JSON inputs return a placeholder result rather than parsed report data.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, and changelog released 2026-05-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
