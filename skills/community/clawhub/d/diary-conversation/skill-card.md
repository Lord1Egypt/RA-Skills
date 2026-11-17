## Description:

通过自然对话引导用户记录每日生活，生成散文式日记并支持图片上传。使用场景：当用户想要记录日记、回顾一天、写日记、记录今天、daily journal、生活记录时触发此技能。自动组织日记和图片，生成连贯的散文叙事。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinrenkun4916-hash](https://clawhub.ai/user/yinrenkun4916-hash)

### License/Terms of Use:


## Use Case:

People who want a personal journaling assistant use this skill to turn a short natural conversation about their day into a polished diary entry. It can also organize related images and save the entry as local Markdown with index metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal reflections, mood details, keywords, and photos may be saved in the local journals directory.

Mitigation: Review the storage location before use and delete or encrypt sensitive diary entries and images as needed.

Risk: Backups, Git, or cloud sync can copy private diary data outside the immediate workspace.

Mitigation: Enable syncing or backups only deliberately and confirm that the destination is appropriate for private journal content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinrenkun4916-hash/skills/diary-conversation)
- [Diary format guide](references/diary-formats.md)
- [File storage guide](references/file-storage.md)
- [Image handling guide](references/image-handling.md)
- [Question template guide](references/question-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown diary entries with local file paths and JSON index metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local journals directory containing diary Markdown, image files, thumbnails, and index data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
