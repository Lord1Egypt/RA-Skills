## Description:

Transform articles, blog posts, reports, or any text content into self-contained HTML infographics with multiple layout styles and optional PNG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengsh0923](https://clawhub.ai/user/fengsh0923)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn URLs, files, or pasted article text into visual summaries, data dashboards, timelines, comparisons, process flows, or editorial-style infographics. The skill guides the agent through outline, layout, style, illustration, and output-format confirmations before generating the final asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional PNG export may install browser tooling and render active HTML with network access.

Mitigation: Use HTML-only mode or run PNG export in an isolated environment with preinstalled, pinned Playwright and Chromium unless export is specifically needed.

Risk: Rendering untrusted article content or generated HTML can expose sensitive content or external font and network requests during export.

Mitigation: Avoid rendering sensitive or untrusted content with external fonts or network access enabled; review generated HTML before export.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengsh0923/skills/article-to-infographic)
- [Style Presets](artifact/references/style-presets.md)
- [Illustration Integration Guide](artifact/references/illustrations-guide.md)
- [Open Peeps](https://www.openpeeps.com/)
- [unDraw](https://undraw.co/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus self-contained HTML and optional PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended to include inline CSS and JavaScript, print-ready styling, responsive layouts, and optional browser-rendered PNG export.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
