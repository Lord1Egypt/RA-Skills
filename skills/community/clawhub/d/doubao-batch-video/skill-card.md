## Description: <br>
豆包网页视频批量生成技能，帮助代理基于豆包网页端批量生成推广视频，并完成文案创作、视频生成、拼接混音和压缩输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to guide an agent through batch short-video creation with Doubao, including prompt drafting, required user confirmation, browser-based generation, and local ffmpeg post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can operate an authenticated Doubao browser session and consume generation quota. <br>
Mitigation: Use a dedicated browser profile for Doubao, confirm the account context before generation, and monitor quota use. <br>
Risk: Generated prompts and browser actions could submit unintended or sensitive content to Doubao. <br>
Mitigation: Review and approve all prompts before generation, as the skill requires a user confirmation step. <br>
Risk: The workflow downloads generated videos and writes media files locally. <br>
Mitigation: Run it in a known working directory, review output paths, and avoid using sensitive local files as inputs. <br>
Risk: Local post-processing depends on ffmpeg and ffprobe behavior. <br>
Mitigation: Use trusted ffmpeg builds and inspect the generated MP4 outputs before publishing or uploading them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hitjcl/doubao-batch-video) <br>
- [Doubao web app](https://www.doubao.com/) <br>
- [Doubao video generator](https://www.doubao.com/video-generator) <br>
- [豆包网页端登录与自动化参考](references/doubao-login.md) <br>
- [GEO 视频生成提示词参考](references/prompt-references.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash, JSON, JavaScript, and Python command examples; generated media files are produced through external browser and ffmpeg workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompt tables, browser-operation guidance, ffmpeg commands, and local MP4 outputs such as final combined and compressed videos.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
