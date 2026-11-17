## Description:

One-click automated pipeline for AI product launch monitoring with RSS monitoring, product search enrichment, screenshot capture, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a configurable pipeline that monitors AI launch RSS feeds, enriches findings with web search results, optionally captures page screenshots, and produces structured trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default screenshot step opens RSS-provided URLs in a browser without meaningful destination validation.

Mitigation: Review configured feeds, prefer --skip-screenshot, run in a network-restricted sandbox, or add strict URL and redirect validation before enabling screenshot capture.

## Reference(s):

- [AI Launch Pipeline on ClawHub](https://clawhub.ai/terrycarter1985/skills/ai-launch-pipeline)
- [terrycarter1985 ClawHub profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, shell commands]

**Output Format:** [Terminal status text, JSON data files, Markdown analysis report, and optional PNG screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes pipeline outputs under configurable data, analysis, and screenshot directories.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
