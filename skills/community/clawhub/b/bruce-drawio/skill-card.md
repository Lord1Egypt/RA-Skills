## Description: <br>
Generates draw.io diagrams for flowcharts, architecture diagrams, UML diagrams, ER diagrams, mindmaps, network topologies, and other visual diagrams, then exports them through the draw.io CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bruc3van](https://clawhub.ai/user/bruc3van) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other agent users use this skill to turn natural-language diagram requests into editable .drawio files and PNG, SVG, or PDF exports for software architecture, workflows, data modeling, mindmaps, and network documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words could cause unexpected local diagram files or exports. <br>
Mitigation: Ask the agent to confirm output filenames and export format before running, especially for vague requests such as visualize this. <br>
Risk: Capability tags include crypto and can-make-purchases even though the skill is for diagram generation. <br>
Mitigation: Do not provide financial credentials or purchase authority when using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bruc3van/bruce-drawio) <br>
- [draw.io Desktop releases](https://github.com/jgraph/drawio-desktop/releases) <br>
- [diagrams.net editor](https://app.diagrams.net) <br>
- [Best practices reference](references/best-practices.md) <br>
- [Examples reference](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with draw.io XML, .drawio files, and PNG/SVG/PDF exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local draw.io desktop CLI for image export; if it is unavailable, the skill guides installation instead of installing automatically.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
