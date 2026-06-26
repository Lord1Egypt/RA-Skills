## Description: <br>
Auto Create AI Team generates local ai-team folders and Markdown configuration, team-member, progress, and workflow files for single, dual, or custom project team structures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sylvanxiao](https://clawhub.ai/user/sylvanxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to scaffold local AI-team documentation for a project, including team roles, model settings, progress tracking, and workflow notes. It is intended for offline project setup where users want generated Markdown files they can inspect and edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ai-team files can replace or conflict with existing files in a project's ai-team directory. <br>
Mitigation: Run the script on a test copy or review the target ai-team directory before execution, especially when existing project documentation must be preserved. <br>
Risk: Generated WORKFLOW.md content may include data-sharing and automation language that does not match the user's governance expectations. <br>
Mitigation: Review and edit WORKFLOW.md before using it as operational guidance. <br>


## Reference(s): <br>
- [Auto Create AI Team on ClawHub](https://clawhub.ai/sylvanxiao/auto-create-ai-team) <br>
- [Publisher profile](https://clawhub.ai/user/sylvanxiao) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Local Markdown files and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates files under the selected project's ai-team directory using user-selected team type, project type, language, member, and model settings.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
