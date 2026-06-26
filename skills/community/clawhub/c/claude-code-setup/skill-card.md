## Description: <br>
Sets up a project-local .claude/ AI collaboration layer for Claude Code with project instructions, rules, context files, reusable skills, and prompt templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaveLuo](https://clawhub.ai/user/EaveLuo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill when starting Claude Code work in a project that needs a structured .claude/ configuration. It helps initialize and maintain project instructions, coding rules, project context, reusable workflows, and review prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .claude/ files can influence future Claude Code sessions and may encode assumptions that do not fit the target project. <br>
Mitigation: Review generated .claude/ files before relying on them, then adjust project instructions, rules, context, and prompts to match the repository. <br>
Risk: Running the setup from the wrong working directory can create .claude/ in the wrong project. <br>
Mitigation: Identify and switch to the intended project root before running the skill. <br>
Risk: Using --force can replace existing .claude/ files. <br>
Mitigation: Avoid --force unless intentionally refreshing the configuration and after reviewing existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EaveLuo/claude-code-setup) <br>
- [Publisher profile](https://clawhub.ai/user/EaveLuo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, project-local configuration files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates files under the target project's .claude/ directory and skips existing non-empty configurations unless --force is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
