## Description:

Provides developer guidance for using MapV-Three to build 3D map and GIS applications with Z-up coordinates, map editing, measurement tools, feature rendering, data management, route tracking, 3D tiles, and LBS services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahddbing](https://clawhub.ai/user/wahddbing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building Web GIS applications with MapV-Three, especially 3D map editors, measurement tools, spatial data visualizations, route tracking views, and geospatial service integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that use Baidu map credentials can lead developers to expose real API keys in frontend code.

Mitigation: Use restricted keys and avoid embedding secrets or bearer tokens directly in client-side examples.

Risk: Popup and DOM overlay examples can render HTML or feature data supplied by an application.

Mitigation: Sanitize HTML and geospatial feature data before rendering it in popups, labels, or DOM overlays.

Risk: Map editing and delete operations can affect backend data when integrated with a real service.

Mitigation: Require confirmation and authorization checks before applying edit or delete actions to persistent data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wahddbing/skills/bmap-jsapi-three)
- [MapV-Three development guide](SKILL.md)
- [Engine guide](reference/engine.md)
- [Initialization guide](reference/initialization.md)
- [DataSource guide](reference/datasource.md)
- [Editor guide](reference/editor.md)
- [Measure guide](reference/measure.md)
- [3D Tiles loading guide](reference/3dtiles-loading.md)
- [LBS services reference](reference/services.md)
- [DOM overlay guide](reference/dom-overlay.md)
- [Best practices](reference/common/best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples may require Node.js and BMAP_JSAPI_KEY for Baidu map integrations.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
