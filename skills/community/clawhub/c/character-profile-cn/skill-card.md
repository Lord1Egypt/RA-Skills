## Description: <br>
Novel Character Profile Builder (小说人物档案创建工具) is a bilingual CN/EN skill for creating structured, detailed fiction character profiles with Markdown templates, relationship guidance, character arcs, consistency checks, and conflict detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q7766206](https://clawhub.ai/user/q7766206) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External authors and writing teams use this skill to gather character details and produce structured Markdown profiles for protagonists, antagonists, and supporting characters. It also helps organize a LoreBible workspace and review generated profiles for duplicate names, relationship issues, timeline issues, and common-sense consistency concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional workflow runner can evaluate configured Python expressions. <br>
Mitigation: Use only reviewed workflow configuration and avoid custom or modified workflow configs unless they have been inspected. <br>
Risk: The skill can read, write, move, and delete files in the selected workspace. <br>
Mitigation: Run it in a dedicated writing or LoreBible folder and avoid using broad or sensitive directories. <br>
Risk: The --no-confirm option can bypass user confirmation before saving generated content. <br>
Mitigation: Do not use --no-confirm on broad or sensitive directories; review temporary output before moving it into the final character library. <br>
Risk: Generated conflict checks are helper feedback and may miss story, timeline, relationship, or data-integrity issues. <br>
Mitigation: Manually review generated profiles and conflict reports before relying on them in a writing project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q7766206/character-profile-cn) <br>
- [主角塑造详细指南](references/protagonist.md) <br>
- [反派塑造指南](references/antagonist.md) <br>
- [配角设计指南](references/supporting.md) <br>
- [角色关系网络设计](references/relationships.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown profiles with optional JSON configuration and command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated profiles may be saved as Markdown files in a user-selected writing or LoreBible workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
