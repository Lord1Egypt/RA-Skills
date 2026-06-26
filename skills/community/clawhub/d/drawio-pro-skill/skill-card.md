## Description: <br>
Generates draw.io diagrams, flowcharts, architecture diagrams, ER diagrams, UML diagrams, network topologies, ML/DL figures, mind maps, and other visualizations as .drawio XML with local export support for PNG, SVG, PDF, and JPG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and technical writers use this skill to create editable draw.io diagrams for software architecture, data models, workflows, code structure, and other complex systems. It is most useful when diagrams need rich draw.io shapes, custom styling, local exports, or optional Graphviz-assisted layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite diagram and export files in the working directory or a requested output path. <br>
Mitigation: Review requested output paths before running exports and keep generated files in an expected project or artifact directory. <br>
Risk: Code-structure diagram requests may read selected project folders to build import or class graphs. <br>
Mitigation: Run code-visualization flows only on repositories or directories that are appropriate for local analysis. <br>
Risk: Some icon and browser-fallback flows can contact external icon CDNs or diagrams.net. <br>
Mitigation: Use embedded icons or XML-only/local export workflows when offline operation or network minimization is required. <br>
Risk: Style-management flows can store user presets under ~/.drawio-skill/styles. <br>
Mitigation: Inspect or remove saved presets if a shared environment should not retain diagram styling preferences. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agents365-ai/drawio-pro-skill) <br>
- [Auto-layout reference](references/autolayout.md) <br>
- [Diagram type presets](references/diagram-types.md) <br>
- [Shape vocabulary and search](references/shapes.md) <br>
- [Style presets](references/style-presets.md) <br>
- [Style extraction](references/style-extraction.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Shape index attribution](data/SHAPE-INDEX-NOTICE.md) <br>
- [draw.io Desktop releases](https://github.com/jgraph/drawio-desktop/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with XML, JSON, and shell command snippets; local .drawio and exported image or document files when the required tools are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create files in the working directory or requested output path, read selected code folders for code-structure diagrams, and use local draw.io or Graphviz tools when installed.] <br>

## Skill Version(s): <br>
1.14.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
