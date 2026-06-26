## Description: <br>
Helps agents create clear data visualizations with chart selection, color, axes, annotation, and storytelling guidance using inference.sh chart-generation recipes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to select appropriate chart types and generate charts, dashboards, reports, presentations, and data stories with visualization best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a third-party inference.sh CLI and installer. <br>
Mitigation: Install only after deciding that inference.sh is trusted, and prefer the manual checksum-verification path before running infsh commands. <br>
Risk: Chart-generation commands may send datasets or business metrics through the infsh provider. <br>
Mitigation: Avoid confidential datasets, customer records, and sensitive business metrics unless the provider's account, billing, and data-handling terms are acceptable. <br>
Risk: Visualization guidance can still produce misleading charts if applied to the wrong data shape or audience. <br>
Mitigation: Review generated chart choices, axes, labels, color encodings, and annotations before using the output in reports or presentations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okaris/data-visualization-2) <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash, Python, and HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include infsh commands that generate chart image files through the inference.sh CLI.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
