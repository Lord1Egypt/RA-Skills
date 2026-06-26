## Description: <br>
Helps teams manage changes to an existing or in-progress feature by assessing impact, updating feature documentation incrementally, and creating a CR-numbered change task plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cping6](https://clawhub.ai/user/cping6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product engineers, and product architects use this skill when a planned or already developed feature needs a scoped modification, extension, or direction change. It guides impact analysis, incremental documentation updates, CR numbering, and generation of a change-specific task plan without implementing business code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose changes to requirements, technical plans, and task plans based on existing project files, so incorrect assumptions may lead to misleading downstream work. <br>
Mitigation: Review the impact analysis and generated CR task plan before applying changes or handing work to an implementation skill. <br>
Risk: The available security scan reported no suspicious behavior but noted that the artifact was not independently reviewed in that scan context. <br>
Mitigation: Verify the installed skill files and requested file access before use, especially in repositories with sensitive product plans or code. <br>


## Reference(s): <br>
- [Feature Evolution Template](artifact/assets/feature-evolution-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cping6/feature-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown change records, impact analysis, documentation updates, and incremental task plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read existing feature requirements, technical plans, task plans, project context, and related code to assess change impact; does not write business implementation code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
