## Description:

小说章节配图生成器。自动检索项目中的角色设定和已有插画，为指定章节生成风格统一、角色一致的插图Prompt。AI按需判断是否添加漫画文字层（无气泡无字框）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and writing-focused agent users use this skill to turn novel chapters or scene excerpts into consistent illustration prompts. It searches for character references, style history, and prior illustration notes, then proposes 1-3 scene prompts aligned to the chapter's mood.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan a broad project area while looking for character descriptions, style references, and prior illustration records.

Mitigation: Use it only in novel-writing projects where that search is expected, and provide explicit chapter and reference paths before execution.

Risk: The skill may write reusable character data or other project outputs without narrow limits.

Mitigation: Require confirmation and a specific output file before any project write-back.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fslong520/skills/brushtrace)
- [Publisher Profile](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, JSON, and plain text illustration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1-3 structured prompts and may include an optional comic text layer with placement, font, and scene-integration guidance.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
