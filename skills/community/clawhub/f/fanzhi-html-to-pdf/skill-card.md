## Description:

Converts local HTML pages into PDF files with Puppeteer and an installed Chrome or Chromium browser, including support for Chinese text, ECharts rendering waits, hidden content expansion, content-height measurement, whitespace reduction, and page-break avoidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ronie-shi](https://clawhub.ai/user/ronie-shi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents in converting dashboard, report, or web-page HTML into PDF output from a local environment. It is especially oriented to Chinese-language reports and pages with rendered charts, tabs, animations, or collapsible sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied HTML is rendered in Chromium with the browser sandbox disabled by default.

Mitigation: Use trusted HTML only, or run the conversion inside a disposable or containerized environment and remove or explicitly opt in to --no-sandbox.

Risk: Output-path controls are weak and an existing file may be overwritten.

Mitigation: Choose output paths deliberately, review the resolved destination before running, and avoid running the converter with elevated privileges.

Risk: Dependencies are not pinned by a lockfile in the supplied artifact.

Mitigation: Pin npm dependencies before deployment and review dependency updates before reinstalling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ronie-shi/skills/fanzhi-html-to-pdf)
- [Chromium and Chrome platform paths](references/platforms.md)
- [Sources and dependency licenses](references/sources.md)
- [HTML to PDF technical details](references/tech-details.md)
- [Puppeteer](https://github.com/puppeteer/puppeteer)
- [pdf-lib](https://github.com/Hopding/pdf-lib)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated PDF is expected to be a single-page, image-like rendering of the HTML rather than searchable or selectable text.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
