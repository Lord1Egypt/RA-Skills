## Description:

Generate publication-quality chart images from data for line, bar, area, point, histogram, candlestick, pie/donut, heatmap, multi-series, and stacked visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to generate chart image files from JSON, CSV, stdin, or custom Vega-Lite specs for reports, dashboards, alerts, and chat attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdated rendering dependencies have current security advisories.

Mitigation: Upgrade Sharp and Vega-family dependencies before installation or deployment, then rerun package audit and release security review.

Risk: Untrusted chart specs, CSV file inputs, or output paths may cause unsafe file access or unexpected rendering behavior.

Mitigation: Keep --spec, --csv-file, and --output controlled by trusted runtime code, and pass chart data through structured argv or trusted temporary files.

Risk: Shell-built commands around user-controlled JSON, titles, labels, or paths can introduce command injection risk.

Mitigation: Use argv-style process execution and avoid sh -c, command substitution, and inline echo patterns for untrusted chart inputs.

## Reference(s):

- [Chart Image on ClawHub](https://clawhub.ai/dannyshmueli/skills/chart-image)
- [Vega-Lite Documentation](https://vega.github.io/vega-lite/)
- [Sharp Documentation](https://sharp.pixelplumbing.com/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [PNG or SVG image files, with concise Markdown or text guidance for invocation and delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is PNG; SVG output is optional; output paths should be controlled by trusted runtime code.]

## Skill Version(s):

2.6.35 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
