## Description: <br>
Official Emergence Science Skill for rendering professional diagrams (TikZ, Mermaid, Graphviz, D2) via the Emergence Science Render API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and autonomous agents use this skill to render structured TikZ, Mermaid, Graphviz, and D2 diagram code into technical visuals through the Emergence Science Render API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram source is sent to Emergence Science servers with a user-provided API key. <br>
Mitigation: Avoid sending secrets, proprietary architecture, private source code, personal data, or regulated information in diagrams. <br>
Risk: Autonomous or repeated rendering calls can consume account credits and may hit the service rate limit. <br>
Mitigation: Monitor credit usage, add caller-side limits, and respect the 1-minute per-account rate limit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emergencescience/emergence-render-image) <br>
- [Emergence Science Web UI](https://emergence.science/) <br>
- [Emergence Render API Endpoint](https://api.emergence.science/tools/render) <br>
- [Emergence Render OpenAPI Schema](https://api.emergence.science/tools/render/openapi.json) <br>
- [Emergence Content Index](https://emergence.science/content/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Files, Configuration instructions] <br>
**Output Format:** [JSON responses with base64-encoded PNG or SVG image data, plus diagram source code and setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EMERGENCE_API_KEY; supports TikZ, Mermaid, Graphviz, and D2; render responses may take up to 1 minute.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
