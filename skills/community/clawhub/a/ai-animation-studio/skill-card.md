## Description: <br>
AI Animation Studio helps an agent turn a user story into an animated video workflow with storyboarding, Doubao-backed image and video generation, voiceover, subtitles, BGM selection, and FFmpeg composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to guide an agent through short animated video production from a written story, including style selection, scene planning, media generation, audio selection, and final video assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story prompts and image references may be sent to Doubao/Volcengine-backed media generation services. <br>
Mitigation: Use the skill only with content approved for that provider and avoid entering sensitive or confidential story details unless the deployment policy permits it. <br>
Risk: Media generation and text-to-video calls may consume API quota or create provider costs. <br>
Mitigation: Confirm ARK_API_KEY configuration, quota limits, and expected cost before running full multi-scene workflows. <br>
Risk: The workflow depends on local paths for doubao-media and D:\AI视频资源 media assets. <br>
Mitigation: Verify those paths point to trusted local resources and keep the media folder limited to assets intended for the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/systiger/ai-animation-studio) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [BGM_LIBRARY.md](artifact/BGM_LIBRARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with command examples, JSON planning artifacts, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MP4 video outputs, subtitles, voiceover audio, selected BGM, and intermediate image or video assets when required tools and local media resources are available.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
