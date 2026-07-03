## Description: <br>
Drawio Studio helps agents create editable draw.io / diagrams.net technical diagrams, including architecture diagrams, ERDs, UML, sequence diagrams, flowcharts, ML diagrams, brand-symbol diagrams, and code-structure maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, architects, and technical writers use this skill to plan, generate, validate, and export editable technical diagrams while preserving .drawio sources for later maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive architecture, customer, or regulated data may leave the local boundary if diagrams.net URL handoff or networked brand-icon rendering is used. <br>
Mitigation: Use local .drawio files and local lint/export first; only create diagrams.net URLs or network-rendered brand icons when the external data boundary is acceptable. <br>
Risk: Optional local tools such as Graphviz or draw.io Desktop may be unavailable, which can prevent automatic layout or export. <br>
Mitigation: Downgrade to editable source delivery, URL fallback, or manual layout, and report any dependency that could not be verified. <br>
Risk: Brand icons and shape indexes include third-party assets and trademarks. <br>
Mitigation: Keep third-party notices with redistributed packages and verify upstream licensing or trademark constraints before public or commercial use of branded symbols. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bovinphang/skills/fec-drawio-studio) <br>
- [Publisher Profile](https://clawhub.ai/user/bovinphang) <br>
- [Data Residency](references/data-residency.md) <br>
- [Diagram Patterns](references/diagram-patterns.md) <br>
- [Flowchart Quality](references/flowchart-quality.md) <br>
- [XML And Mermaid](references/xml-and-mermaid.md) <br>
- [Third Party Notices](data/THIRD_PARTY_NOTICES.md) <br>
- [diagrams.net Viewer](https://viewer.diagrams.net/) <br>
- [diagrams.net Editor](https://app.diagrams.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated .drawio/XML, Mermaid, CSV, URL, or exported diagram artifacts as needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local .drawio sources, PNG/SVG/PDF/JPG exports, diagrams.net URLs, layout manifests, and verification status.] <br>

## Skill Version(s): <br>
2.8.0 (source: package.json, README.md, artifact/metadata.json, evidence.release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
