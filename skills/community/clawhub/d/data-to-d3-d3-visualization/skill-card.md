## Description:

Build deterministic, verifiable D3.js visualizations from local data files as standalone HTML, SVG, and optional PNG outputs without external network dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to convert local CSV, TSV, or JSON data into reproducible D3 charts for reports, web pages, and data-driven SVG output. It is most useful when charts need fixed dimensions, deterministic ordering, offline dependencies, legends, axes, tooltips, or optional exported raster images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tooltip examples render data-derived content as browser HTML, which can execute untrusted markup when visualization data is not trusted.

Mitigation: Use trusted data only, or change tooltip rendering to text nodes or sanitized HTML before serving generated outputs.

Risk: The skill description references D3.js v6 while the determinism guidance defaults to d3@7.9.0, which can affect reproducible builds.

Mitigation: Choose and pin a single D3 version in generated outputs and lockfiles before relying on deterministic builds.

Risk: Generated interactive HTML can run in the browser context where it is hosted.

Mitigation: Do not serve generated visualizations from authenticated or sensitive origins until tooltip rendering is fixed and outputs are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/data-to-d3-d3-visualization)
- [Publisher profile](https://clawhub.ai/user/wu-uk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JavaScript, HTML, and CSS code, plus local HTML, SVG, and optional PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be deterministic, offline, and written under a predictable dist/ folder unless the user specifies another path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
