## Description: <br>
A bridge between AI and building data for reading and creating BIM models using code-like CSV and SVG workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novashang](https://clawhub.ai/user/novashang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, BIM modelers, and AI coding agents use this skill to create, inspect, validate, render, and optionally publish BimDown building models from briefs or existing plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external bimdown-cli npm package. <br>
Mitigation: Confirm the package source and obtain user permission before installing or running privileged global npm installation commands. <br>
Risk: Publishing uploads the project directory, including CSV, SVG, GLB files, filenames, room names, geometry, and notes, to a sharing endpoint. <br>
Mitigation: Review the project for confidential information and ask for explicit user approval before the first publish. <br>
Risk: The publish destination can be changed with BIMCLAW_API or --api. <br>
Mitigation: Confirm the configured endpoint before publishing, especially when an override is present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/novashang/bimdown-cli) <br>
- [Publisher profile](https://clawhub.ai/user/novashang) <br>
- [BimClaw publish endpoint](https://bim-claw.com/api/shares/publish) <br>
- [Building Design SOP](artifact/references/building-design.md) <br>
- [BIM Modeling SOP](artifact/references/bim-modeling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and BIM CSV/SVG file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local BimDown project files and may optionally request user approval to publish a zipped project for web preview.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
