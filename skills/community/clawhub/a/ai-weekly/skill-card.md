## Description:

Generates a searchable, filterable weekly AI news report from public RSS feeds as a standalone HTML page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and teams use this skill to collect the week's AI news and review a sourced, searchable report with optional model rankings and market context. A brief Markdown news summary is also available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deployment, Feishu publishing, and scheduler tools can publish reports or change hosting settings.

Mitigation: Invoke these tools only with explicit authorization; use least-privilege, short-lived tokens and leave scheduled push disabled unless unattended publication is intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/elisabeth15501/skills/ai-weekly)
- [Project homepage (declared in metadata)](https://github.com/Elisabeth15501/ai-weekly)
- [Data sources](references/data_sources.md)
- [Report structure](references/report_structure.md)

## Skill Output:

**Output Type(s):** [HTML report, Markdown summary, Guidance]

**Output Format:** [Standalone HTML file or Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML reports support search, filtering, and dark mode; publication is optional and separate from report generation.]

## Skill Version(s):

4.1.6 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
