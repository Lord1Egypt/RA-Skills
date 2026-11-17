## Description:

Auto Create Skill identifies repeatable workflows from a conversation and generates or updates reusable Skill files so an agent can repeat the process with user-supplied parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxilong-43](https://clawhub.ai/user/zhangxilong-43)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn repeated conversational workflows into structured Skill files, update previously generated skills, and manage a registry of those generated workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and edit persistent skill directories.

Mitigation: Install only when persistent skill creation is intended, and review generated triggers, paths, AUTO steps, and shell commands before enabling generated skills.

Risk: Generated workflows may include unsafe shell-style command templates or sensitive write, delete, commit, push, or installation actions.

Mitigation: Require explicit confirmation before writes, deletes, commits, pushes, and installation into agent skill directories.

## Reference(s):

- [Workflow Skill Template](artifact/references/workflow-skill-template.md)
- [ClawHub Skill Page](https://clawhub.ai/zhangxilong-43/skills/auto-create-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify persistent skill directories and registry JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
