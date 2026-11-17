## Description:

Turns Markdown, plain text, images, tables, Excel, and Word inputs into themed single-page HTML, with layout inheritance for already-designed sources and optional publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to convert existing content into a self-contained HTML page, apply one of the built-in themes, set page metadata, and optionally publish the result after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or inherited HTML can carry untrusted content into a page that users may share or publish.

Mitigation: Review generated HTML before sharing it, sanitize inherited HTML, and remove sensitive or unsafe content before publication.

Risk: Private documents or local images may be exposed if they are uploaded or published through external hosting.

Mitigation: Avoid private documents and local images unless the user controls the upload and hosting destination, and require explicit confirmation before publishing.

Risk: The workflow can rely on unpinned dependencies or dynamically loaded third-party chart scripts.

Mitigation: Use trusted or pinned dependencies, and prefer offline or bundled chart assets for sensitive reports.

## Reference(s):

- [easy-html ClawHub page](https://clawhub.ai/songhonglei/skills/easy-html)
- [Live landing page](https://songhonglei.github.io/html-tool-suite/easy-html/)
- [html-tool-suite repository](https://github.com/Songhonglei/html-tool-suite)
- [html-golive theme engine](https://github.com/Songhonglei/html-golive)
- [Design guidance](references/DESIGN.md)
- [Visualization scan guidance](references/VIZ_SCAN.md)
- [Visualization components](references/VIZ_COMPONENTS.md)
- [Chart guidance](references/CHARTS.md)
- [Content structure guidance](references/CONTENT_STRUCTURE.md)
- [Data role conventions](references/DATA_ROLE.md)
- [Style selection guidance](references/STYLES.md)
- [Publishing guidance](references/PUBLISH.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands plus generated HTML, CSS, and JavaScript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained single-page HTML; may use Chart.js CDN fallbacks and publish via html-golive only after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata, SKILL.md, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
