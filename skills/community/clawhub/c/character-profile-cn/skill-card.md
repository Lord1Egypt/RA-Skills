## Description:

Novel Character Profile Builder (小说人物档案创建工具) is a bilingual CN/EN skill for creating structured, detailed fiction character profiles with backstory, personality, relationships, character arcs, consistency checks, protagonist, antagonist, and supporting-character templates, conflict detection, and relationship matrix tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q7766206](https://clawhub.ai/user/q7766206)

### License/Terms of Use:


## Use Case:

External fiction writers and writing-tool users use this skill to plan and generate markdown character profiles for novels and web fiction. It helps structure character identity, appearance, personality, backstory, relationships, story function, and consistency review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration-driven workflow or session files could be tampered with and lead to unintended code execution.

Mitigation: Treat workflow and session JSON as trusted local state, review changes before running the scripts, and install the skill only in a dedicated writing workspace.

Risk: File move or delete behavior could affect unintended content when run against broad project or home directories.

Mitigation: Use a dedicated LoreBible workspace, avoid broad filesystem paths, keep backups of important writing projects, and avoid --no-confirm or quick_creation on important existing work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/q7766206/skills/character-profile-cn)
- [主角塑造详细指南](references/protagonist.md)
- [反派塑造指南](references/antagonist.md)
- [配角设计指南](references/supporting.md)
- [角色关系网络设计](references/relationships.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown profiles and guidance, with Python script commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local character-profile files and LoreBible workspace directories when the bundled scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
