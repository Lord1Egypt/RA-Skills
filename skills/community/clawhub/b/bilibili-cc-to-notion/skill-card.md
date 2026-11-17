## Description:

将B站视频字幕转换为带截图的 Notion 学习笔记，支持 BV 号或完整 URL 输入、字幕下载、内容整理、截图生成、图片上传和 Notion 页面创建。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn Bilibili videos into structured learner-style notes in Notion, including captions, screenshot markers, uploaded images, and a returned Notion page link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run local scripts and external tools while processing video URLs, files, and generated command arguments.

Mitigation: Review the skill before installing, run it in a constrained environment, verify BBDown before execution, and avoid untrusted or specially crafted inputs.

Risk: The skill writes to Notion and can upload local files or archive duplicate pages.

Mitigation: Use a minimally scoped Notion integration, pass only intended files, and confirm the target database and pages before allowing cleanup or archive actions.

Risk: Bilibili authentication may require cookies or account login, which can expose sensitive credentials if mishandled.

Mitigation: Avoid passing sensitive Bilibili cookies unless necessary, keep credentials out of prompts and source files, and prefer temporary, least-privilege credentials where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinyuqinfeng/skills/bilibili-cc-to-notion)
- [BBDown project](https://github.com/nilaoda/BBDown)
- [Notion API documentation](https://developers.notion.com/)
- [Bilibili user space](https://space.bilibili.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like tool results with shell command examples and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Notion page URLs, file upload IDs, processed subtitle segments, screenshot counts, and embedded image counts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
