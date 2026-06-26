## Description: <br>
A diagramming skill for architecture and process visualization that can produce offline layered SVG diagrams or render Mermaid, PlantUML, and Graphviz sources to SVG or HTML with Kroki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[footya](https://clawhub.ai/user/footya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and technical teams use this skill to create architecture diagrams, flowcharts, sequence diagrams, deployment diagrams, and C4-style diagrams for design reviews and technical communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public Kroki or CDN-backed rendering can disclose private diagram content or browser request metadata to third parties. <br>
Mitigation: Use pure offline SVG generation, set --kroki-url to a trusted internal Kroki instance, or avoid CDN-backed HTML previews for sensitive diagrams. <br>
Risk: Generated architecture diagrams can omit or misstate system boundaries, dependencies, or security controls. <br>
Mitigation: Review diagrams against the included architecture checklist and source system documentation before using them in design, review, or operational decisions. <br>


## Reference(s): <br>
- [SVG layered architecture diagram specification](artifact/references/svg-layered-spec.md) <br>
- [Diagram syntax quickstart](artifact/references/diagram-quickstart.md) <br>
- [Architecture diagram quality checklist](artifact/references/architecture-checklist.md) <br>
- [Kroki diagram rendering service](https://kroki.io) <br>
- [ClawHub skill page](https://clawhub.ai/footya/arch-diagrammer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, SVG or HTML files, diagram DSL, and runnable shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local/offline SVG generation or external Kroki/CDN rendering depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, CHANGELOG, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
