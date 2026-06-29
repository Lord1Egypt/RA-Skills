## Description: <br>
Design Swarm provides a structured SOP for 3D renderings, smart-home wiring diagrams, product catalogs, and SVG icon deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers and smart-home project teams use this skill to plan and package visual deliverables, including floor-plan device placement, wiring diagrams, 3D views, product catalog materials, and icon sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create persistent local task files under ~/.workbuddy/tasks and organize outputs under ~/WorkBuddy/design. <br>
Mitigation: Confirm the target directories before running initialization commands and review generated files before sharing them. <br>
Risk: The manifest does not list file-write permission even though the instructions create task files. <br>
Mitigation: Require explicit user approval for file creation or ask the publisher to add a narrow file-write permission before deployment. <br>
Risk: Generic trigger terms may activate the skill in broad design conversations. <br>
Mitigation: Narrow activation triggers or confirm intent before using the workflow for a project. <br>
Risk: Wiring plans and 3D renderings may not reflect actual site conditions. <br>
Mitigation: Have site-specific wiring and external deliverables reviewed by a qualified human before customer use. <br>


## Reference(s): <br>
- [Design Swarm ClawHub listing](https://clawhub.ai/gaoshung1981888/design-swarm) <br>
- [Publisher profile](https://clawhub.ai/user/gaoshung1981888) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file templates, and deliverable specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to create local task files and organize design deliverables in user project directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
