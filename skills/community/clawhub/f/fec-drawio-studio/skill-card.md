## Description: <br>
Drawio Studio helps agents create editable draw.io and diagrams.net technical diagrams with shape lookup, brand symbols, auto-layout, code structure maps, validation, and export fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to produce editable architecture diagrams, ERDs, UML and sequence diagrams, flowcharts, ML diagrams, and code structure maps. It is suited for workflows that need durable .drawio sources, diagram validation, official shape lookup, or export fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive diagrams may cross an external data boundary when diagrams.net URL handoff or networked brand-icon fetching is used. <br>
Mitigation: Use local .drawio output and local lint/export for sensitive architecture, customer, or regulated data; use URL handoff, external icon fetching, or a self-hosted diagrams.net base URL only when that boundary is acceptable. <br>
Risk: Optional external tools such as Graphviz and draw.io Desktop may be unavailable or unverified in the runtime environment. <br>
Mitigation: Downgrade to local .drawio source delivery, saved graph JSON, or diagrams.net URL fallback instead of installing tools automatically. <br>
Risk: Third-party shape indexes and brand icon manifests may carry upstream license or trademark constraints. <br>
Mitigation: Keep the bundled third-party notices with redistributed packages and review upstream terms before using brand marks in deliverables. <br>
Risk: Generated diagrams can contain misleading structure, clipped labels, overlapping layouts, or broken connections. <br>
Mitigation: Run diagram linting where available and manually review the opened diagram for traceable connections, readable labels, and non-overlapping layout before handoff. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/skills/fec-drawio-studio) <br>
- [Data Residency](references/data-residency.md) <br>
- [Diagram Patterns](references/diagram-patterns.md) <br>
- [Flowchart Quality](references/flowchart-quality.md) <br>
- [XML And Mermaid](references/xml-and-mermaid.md) <br>
- [Third Party Notices](data/THIRD_PARTY_NOTICES.md) <br>
- [diagrams.net Viewer](https://viewer.diagrams.net/) <br>
- [diagrams.net Editor](https://app.diagrams.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with draw.io XML or .drawio sources, JSON manifests, shell commands, and optional exported diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local .drawio sources, structural verification results, PNG/SVG/PDF/JPG exports, and diagrams.net URLs when the external data boundary is acceptable.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence, package.json, README.md, metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
