## Description: <br>
Anime Drama converts novel or story text into vertical anime-style short videos by generating a shot script, creating RunningHub images and video clips, and merging clips with ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickSF](https://clawhub.ai/user/rickSF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation agents use this skill to turn plain story text into a resumable anime short-video workflow with storyboard JSON, generated image assets, generated video clips, and a final vertical MP4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story text and generated images may be sent to RunningHub and stored locally during processing. <br>
Mitigation: Use only story text and generated assets that are acceptable to send to RunningHub and retain in local output directories. <br>
Risk: The submitted script runs shell command strings built from workflow inputs. <br>
Mitigation: Review before installation, avoid untrusted or adversarial story text, and prefer a maintainer update that replaces shell=True command strings with argument-list subprocess calls. <br>
Risk: RunningHub API keys can appear in command strings. <br>
Mitigation: Use scoped credentials where available, avoid sharing logs, and prefer a maintainer update that redacts API keys from process and error output. <br>


## Reference(s): <br>
- [Pipeline Usage](references/pipeline-usage.md) <br>
- [FFmpeg Install](references/ffmpeg-install.md) <br>
- [RunningHub AI App Notes](references/runninghub-ai-app-notes.md) <br>
- [RunningHub Upload API](https://www.runninghub.cn/task/openapi/upload) <br>
- [ClawHub Release Page](https://clawhub.ai/rickSF/anime-drama) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [JSON storyboard, PNG images, MP4 videos, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNNINGHUB_API_KEY, RunningHub image and video app IDs, python3, curl, ffmpeg, and the runninghub skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
