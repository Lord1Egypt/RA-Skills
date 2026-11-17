## Description:

使用 AI Hive Seedance 2.5 将中文短视频创作迁移为可复用分镜，并支持文生视频、图生视频、参考素材生成、视频编辑与延长。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to generate Chinese vertical short-video prompts and run AI Hive Seedance 2.5 video workflows as an alternative to Dreamina-style creation. It helps structure three-beat storyboards, configure API credentials, submit generation jobs, upload approved media, query tasks, and download generated results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, API credentials, and selected media files are sent to AI Hive for generation workflows.

Mitigation: Install and run the skill only when that data sharing is acceptable; keep the API key private and prefer a dedicated virtual environment.

Risk: Generated result downloads should be treated cautiously because evidence notes a file-download hardening issue around server-provided task types.

Mitigation: Use a non-sensitive output directory and review downloaded files; harden filename sanitization before broader deployment.

Risk: Generated video may contain unstable subject identity, product details, visible text, or unsafe caption areas for vertical social platforms.

Mitigation: Review source-media authorization, generated outputs, subtitle safe zones, and final frames before publishing or stitching clips.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/dreamina-video-generation-alternative)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown guidance with inline bash commands and CLI JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can submit AI Hive video tasks, upload image/video/audio media, query task status, and save generated media files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
