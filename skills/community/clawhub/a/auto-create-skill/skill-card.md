## Description: <br>
Auto Create Skill helps agents identify repeatable workflows from conversation and generate or update reusable Skill files for later execution with key parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxilong-43](https://clawhub.ai/user/zhangxilong-43) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn recurring conversational workflows into reusable Claude-compatible Skills, and to list or update Skills created by the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify persistent future agent behavior through generated Skills and broad trigger phrases. <br>
Mitigation: Review generated Skill files, trigger phrases, and installation paths before enabling or sharing them. <br>
Risk: Generated workflows may include high-impact repository actions such as editing code, deleting files, committing, or pushing. <br>
Mitigation: Require explicit confirmation checkpoints for high-impact steps and inspect proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangxilong-43/auto-create-skill) <br>
- [Workflow skill template](references/workflow-skill-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown skill files with inline shell commands and JSON registry entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write SKILL.md files and registry JSON in supported Claude environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
