## Description: <br>
Generate D2 diagram code and optional image exports for flowcharts, system architecture diagrams, organizational charts, service topology diagrams, state machines, swimlanes, sequence diagrams, SQL table relationships, and grid diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huta0kj](https://clawhub.ai/user/huta0kj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical writers use this skill to turn natural-language diagram requests into validated D2 source and optional SVG, PNG, or text previews. It is intended for workflows that need structured architecture, process, database, sequence, topology, state, swimlane, organization, or grid diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local D2 and Python commands to validate, export, and post-process diagram files. <br>
Mitigation: Review commands before execution, install dependencies from trusted package managers, and generate outputs in a dedicated workspace. <br>
Risk: The Tala SVG path includes mandatory removal of an 'UNLICENSED COPY' watermark. <br>
Mitigation: Avoid Tala SVG export unless the user has confirmed that the installed Tala license permits watermark removal. <br>
Risk: Diagram prompts and generated files may contain confidential architecture, process, or database details. <br>
Mitigation: Keep generated files local and avoid online diagram playgrounds for confidential diagrams. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huta0kj/d2-diagram-creator) <br>
- [D2 installation documentation](https://github.com/terrastruct/d2/blob/master/docs/INSTALL.md) <br>
- [Tala layout engine](https://github.com/terrastruct/tala) <br>
- [D2 syntax reference](references/syntax.md) <br>
- [D2 CLI help reference](references/cli_help.md) <br>
- [Flowchart guide](references/diagram-types/flowchart.md) <br>
- [System architecture guide](references/diagram-types/architecture.md) <br>
- [SQL table relationship guide](references/diagram-types/sql-table.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary with D2 code files and optional SVG, PNG, or ASCII preview files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the local D2 CLI for validation and export when image or preview output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
