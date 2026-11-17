## Description:

生成电影感运镜短视频脚本的技能。输出含逐秒分镜拆解、运镜参数和BGM卡点节奏的完整脚本及一键视频提示词，支持上传图片或文字描述生成，可直接用于实拍或AI视频生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, photographers, directors, video editors, and AI video users use this skill to turn an image or scene description into a cinematic camera-movement script, beat-synced storyboard, filming guidance, and video-generation prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes review-worthy direct video generation behavior through an external workflow and RedFoxHub API key.

Mitigation: Prefer script and prompt generation unless the external video-generation workflow is trusted, and store REDFOX_API_KEY in a secure secret manager or tightly permissioned environment variable.

Risk: Shell-oriented guidance or command examples could mishandle prompts or other user-provided text.

Mitigation: Pass prompts through safe argument handling rather than interpolating untrusted text into shell strings.

Risk: Generated people descriptions may introduce unwanted demographic defaults.

Mitigation: Review generated character descriptions before filming or video generation and adjust demographic attributes to match the intended scene.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/cinematic-camera-script)
- [Camera movement reference](artifact/references/camera-movements.md)
- [Shot composition reference](artifact/references/shot-composition.md)
- [BGM sync reference](artifact/references/bgm-sync.md)
- [AI prompt reference](artifact/references/ai-prompts.md)
- [Core workflow](artifact/references/core_workflow.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with structured storyboard sections, camera parameters, filming guidance, and copy-ready video prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional direct-video-generation guidance that depends on REDFOX_API_KEY and the seedance-video-gen workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
