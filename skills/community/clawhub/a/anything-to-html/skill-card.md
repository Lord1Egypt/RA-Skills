## Description:

Anything to HTML helps an agent turn reports, analyses, plans, reviews, notes, and similar deliverables into a single browser-openable HTML file with structured layout, inline styling, semantic markup, and optional lightweight visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysredcity](https://clawhub.ai/user/ysredcity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, product teams, and business users use this skill when an agent's final deliverable should be a polished, shareable HTML document instead of a long Markdown response. It is suited for research reports, data summaries, design notes, plans, reviews, meeting notes, one-page summaries, and product-interface mockups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may optionally load third-party CDN scripts when opened.

Mitigation: For sensitive business data, instruct the agent to avoid CDN scripts and use inline SVG or native JavaScript instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysredcity/skills/anything-to-html)
- [Design tokens](references/design-tokens.md)
- [Article archetype guide](references/archetype-article.md)
- [Dashboard archetype guide](references/archetype-dashboard.md)
- [Poster archetype guide](references/archetype-poster.md)
- [App screen archetype guide](references/archetype-app-screen.md)
- [Tailwind browser CDN](https://cdn.tailwindcss.com)
- [ECharts CDN](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js)
- [D3 CDN](https://cdn.jsdelivr.net/npm/d3@7)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Single-file HTML guidance and code, usually delivered as one complete .html document with inline CSS and optional inline or allowlisted JavaScript.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are designed to open directly in a browser and to remain readable as structured text for later agent processing.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
