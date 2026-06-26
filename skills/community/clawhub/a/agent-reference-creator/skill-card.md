## Description: <br>
Creates normative OpenClaw reference files that define narrow agent professions, responsibilities, boundaries, routing cues, and required documentation structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodrigo09313](https://clawhub.ai/user/rodrigo09313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent architects, and OpenClaw knowledge-base maintainers use this skill to interview users, validate specialization boundaries, and produce reusable reference documents for agent professions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reference files can influence future OpenClaw agent behavior, specialization boundaries, and routing. <br>
Mitigation: Review generated reference files before relying on them in the OpenClaw knowledge base. <br>
Risk: The installer can copy files into an OpenClaw KB skill directory and overwrite an existing installation after user confirmation. <br>
Mitigation: Run the installer only against the intended OpenClaw KB path and inspect the target directory before confirming overwrite. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rodrigo09313/agent-reference-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reference files with YAML frontmatter and structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for OpenClaw KB/references/[specialization].md and should be reviewed before they shape agent creation or routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
