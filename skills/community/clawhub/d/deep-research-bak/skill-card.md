## Description:

Deep Research.Bak guides agents through multi-source research, citation tracking, verification, and report packaging for comprehensive citation-backed research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emiltsoi](https://clawhub.ai/user/emiltsoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research users use this skill to conduct comprehensive research, compare technologies or markets, and package citation-backed Markdown, HTML, and PDF reports with validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local reports and state files and may auto-open generated HTML or PDF outputs.

Mitigation: Use only research topics and output locations that are acceptable to store locally, and approve file writes or auto-open behavior before execution.

Risk: Long reports can spawn continuation agents, expanding work beyond the initial response.

Mitigation: Review the requested scope and continuation state before allowing additional agent runs.

Risk: Optional third-party search tooling can require API keys and additional dependencies.

Mitigation: Do not configure provider keys or install optional search tooling unless the dependencies are trusted and pinned.

Risk: Citation and HTML handling can be unsafe with untrusted Markdown or unreviewed generated content.

Mitigation: Avoid untrusted Markdown inputs and review generated citations, HTML, and PDF output before opening or sharing them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/emiltsoi/skills/deep-research-bak)
- [Deep Research Methodology](reference/methodology.md)
- [Report Assembly](reference/report-assembly.md)
- [Quality Gates and Standards](reference/quality-gates.md)
- [HTML Generation](reference/html-generation.md)
- [Auto-Continuation Protocol](reference/continuation.md)
- [WeasyPrint PDF Generation Guidelines](reference/weasyprint_guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional HTML and PDF file exports, plus inline shell commands and validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persisted citation state, bibliography data, and generated report files under user-approved local paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
