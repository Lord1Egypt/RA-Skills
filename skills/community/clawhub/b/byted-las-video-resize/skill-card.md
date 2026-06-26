## Description: <br>
Resizes and scales video resolution using Volcengine LAS with GPU NVENC encoding, configurable dimension bounds, aspect-ratio handling, async submit-poll execution, and batch workflow support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media workflow operators use this skill to resize, upscale, downscale, transcode, or batch-process videos through Volcengine LAS. It guides users through credential checks, price estimation, LAS task submission, polling, and result presentation. <br>

### Deployment Geography for Use: <br>
Global, with execution configured for supported Volcengine LAS regions such as cn-beijing and cn-shanghai. <br>

## Known Risks and Mitigations: <br>
Risk: Environment setup can install or update remote SDK code before execution. <br>
Mitigation: Review, pin, or disable the automatic SDK install/update step before installing or running the skill. <br>
Risk: The workflow requires LAS credentials and may use TOS credentials when downloading outputs from TOS. <br>
Mitigation: Use scoped, temporary credentials and avoid processing sensitive videos unless cloud processing is approved. <br>
Risk: Output filenames or prefixes can overwrite existing TOS objects. <br>
Mitigation: Use unique output directories, filenames, or prefixes for each run and batch. <br>
Risk: A bundled result helper is for unrelated ASR/transcript output rather than video-resize output. <br>
Mitigation: Ignore, remove, or correct that helper before relying on generated result Markdown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-las-video-resize) <br>
- [las_video_resize API Reference](references/api.md) <br>
- [Pricing Reference](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LAS task IDs, TOS output paths, output video details, and pricing disclaimers.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
