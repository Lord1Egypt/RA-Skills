## Description:

用 OpenClaw + Obsidian 搭建内容工厂，系统化生产百万阅读爆文。涵盖选题策略、内容框架、AI 辅助创作、多平台分发、数据分析全流程。适合自媒体创作者、内容团队、个人 IP 建设者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huamu668](https://clawhub.ai/user/huamu668)

### License/Terms of Use:


## Use Case:

Content creators, content teams, and personal-brand operators use this skill to structure an OpenClaw and Obsidian workflow for ideation, drafting, platform adaptation, analytics, and content review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install an unpinned openclaw-multiagent dependency.

Mitigation: Pin and verify the dependency before installation, and install it only from a trusted source.

Risk: Scheduled Daily and Weekly automation may scan sources and write results into an Obsidian vault without clear review controls.

Mitigation: Configure the vault path narrowly, confirm scanned sources and write locations, and enable hooks only after review.

Risk: Generated notes, drafts, and analytics can influence public content decisions if accepted without review.

Mitigation: Review generated content and keep vault backups or version history before publishing or overwriting notes.

## Reference(s):

- [Content Engine release page](https://clawhub.ai/huamu668/skills/content-engine-pin)
- [Obsidian](https://obsidian.md)
- [Topic template](templates/选题模板.md)
- [A/B testing template](templates/AB测试模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and reusable note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Chinese-language workflow guidance, Obsidian vault structure, content templates, and suggested OpenClaw commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
