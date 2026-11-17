## Description: <br>
图表制作大师 helps agents create self-contained dark-theme SVG diagrams for technical documentation across architecture, flow, sequence, structure, mind-map, timeline, explanatory, state-machine, and data-flow formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, technical writers, and project teams use this skill to turn natural-language diagram requests into structured SVG diagram guidance and output for technical documentation. It is intended for normal ClawHub use, with explicit review of output paths and any proposed command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read, exec, and write authority may let the skill propose file access, command execution, or writes beyond the immediate diagram task. <br>
Mitigation: Limit use to diagram generation, require explicit approval for command execution, and review every proposed path before reading from or writing to the workspace. <br>
Risk: The artifact includes an unexplained callback_url field and online font-loading behavior despite local-only claims. <br>
Mitigation: Disable or remove callback handling and online font loading before using sensitive project or architecture details. <br>
Risk: Generated diagrams can expose internal architecture, data flows, or operational details. <br>
Mitigation: Avoid sensitive architecture and internal system details unless the output is reviewed and approved for the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-master-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SVG code examples, command snippets, and optional JSON-style status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained SVG diagram artifacts or instructions for saving them to explicit output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
