## Description:

Conduct structured web research by searching, fetching, and synthesizing information into reports with citations and source verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to run structured web research workflows that search, fetch, deduplicate, score, and synthesize sources into cited reports for single questions or small batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may embed untrusted web content as executable HTML when opened.

Mitigation: Prefer Markdown or JSON output for untrusted research topics, or escape dynamic content and validate URLs before opening or sharing HTML reports.

Risk: Research outputs may include outdated, incomplete, disputed, or weakly sourced claims.

Mitigation: Review cited sources, cross-reference major claims, check publication dates for time-sensitive topics, and preserve limitations in the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigas/skills/claw-web-research)
- [Search Strategies for Web Research](artifact/references/search-strategies.md)
- [Synthesis Framework](artifact/references/synthesis-framework.md)
- [Research Report Template](artifact/references/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, guidance]

**Output Format:** [Markdown, JSON, or self-contained HTML research reports with source lists, quality scoring, limitations, and methodology notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written to workspace/research/ by default; batch mode accepts a JSON file of research questions.]

## Skill Version(s):

2.1.0 (source: release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
