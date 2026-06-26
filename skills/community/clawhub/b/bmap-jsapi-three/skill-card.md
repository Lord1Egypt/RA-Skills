## Description: <br>
Helps developers build 3D map and GIS applications with MapV-Three, including engine setup, Baidu Maps integration, data sources, feature drawing, measurement tools, overlays, 3D tiles, and geospatial visualization patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahddbing](https://clawhub.ai/user/wahddbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GIS engineers use this skill as a MapV-Three reference for implementing browser-based 3D mapping workflows, including map initialization, spatial data rendering, editing, measurement, model loading, trackers, and map service integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Popup, DOM overlay, or DOMPoint examples may insert untrusted GeoJSON, CSV, or API fields into HTML strings. <br>
Mitigation: Escape or sanitize untrusted fields before assigning HTML, and prefer safe DOM APIs such as textContent when rendering user-controlled content. <br>
Risk: Map service API keys can be exposed or overused if embedded directly in shared client code. <br>
Mitigation: Keep BMAP_JSAPI_KEY scoped and private, apply provider-side restrictions, and avoid committing real keys in examples or configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wahddbing/bmap-jsapi-three) <br>
- [MapV-Three skill guide](artifact/SKILL.md) <br>
- [MapV Three initialization guide](artifact/reference/initialization.md) <br>
- [Engine guide](artifact/reference/engine.md) <br>
- [Editor guide](artifact/reference/editor.md) <br>
- [Measure guide](artifact/reference/measure.md) <br>
- [DOM overlay guide](artifact/reference/dom-overlay.md) <br>
- [Popup guide](artifact/reference/popup.md) <br>
- [Common best practices](artifact/reference/common/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, HTML, CSS, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for package installation examples and BMAP_JSAPI_KEY when using Baidu map services.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
