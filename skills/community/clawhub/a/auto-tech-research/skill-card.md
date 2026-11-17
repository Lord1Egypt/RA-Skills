## Description:

Auto Tech Research helps an agent perform browser-based multi-platform technology research and assemble a structured research report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huayang0704](https://clawhub.ai/user/huayang0704)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical researchers use this skill to research a technology topic across search engines, code hosts, academic sources, communities, and media platforms. The skill organizes findings into a report with topic overview, classified resources, platform statistics, and references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may present fabricated or unverifiable source lists as research evidence.

Mitigation: Treat generated reports as drafts until each source link and claim has verifiable provenance.

Risk: Browser-based research may use authenticated sessions or private links.

Mitigation: Use an isolated browser profile, avoid confidential topics, and require explicit confirmation before authenticated browsing.

Risk: The skill can save generated report files without strong safeguards.

Mitigation: Review generated files before relying on or sharing them, and require confirmation before file writes.

## Reference(s):

- [Auto Tech Research ClawHub page](https://clawhub.ai/huayang0704/skills/auto-tech-research)
- [Platform Search Guide](artifact/references/platform-search-guide.md)
- [Quality Checklist](artifact/references/quality-checklist.md)
- [Markdown Report Template](artifact/references/report-template.md)
- [HTML Report Template](artifact/references/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured research report files, primarily Markdown in the included script and HTML in the documented template workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include source links, platform diagnostics, quality scores, and locally saved output files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog describe 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
