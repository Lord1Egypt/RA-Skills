## Description: <br>
Skill Creator helps agents create, edit, improve, audit, organize, validate, and package OpenClaw AgentSkills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashanzzz](https://clawhub.ai/user/ashanzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to structure OpenClaw AgentSkills, create supporting scripts and references, validate skill metadata, and prepare skills for optional publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify local skill files, which could introduce incorrect or misleading instructions into a published skill. <br>
Mitigation: Name the exact target directory before use, review generated diffs, and scan or validate the skill before deployment. <br>
Risk: This release has malformed frontmatter and confusing install-command text that could propagate into generated metadata. <br>
Mitigation: Verify the package slug, install command, and generated SKILL.md metadata before publishing any skill created with it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ashanzzz/ashan-skill-creator) <br>
- [Workflow Patterns Reference](references/workflow-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local skill directories, SKILL.md files, references, scripts, and packaged skill archives.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
