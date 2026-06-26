## Description: <br>
Course Builder Agent turns lesson text into narrated course videos by generating Chinese slide content, TTS voiceover, subtitles, and MP4 video composition, with optional digital-human narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, trainers, and content creators use this agent to convert lesson scripts or existing course outlines into narrated video courseware. Developers can also use it as a local media pipeline that creates slides, audio, subtitles, and final MP4 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lesson text or photos may be sent to TTS or digital-human providers when those options are used. <br>
Mitigation: Avoid confidential course material and personal photos unless the provider privacy and retention terms are acceptable. <br>
Risk: The skill runs local media tools and writes generated video artifacts. <br>
Mitigation: Run it in a controlled workspace, review requested inputs and outputs, and confirm ffmpeg, ffprobe, edge-tts, and Python package installation are acceptable before use. <br>


## Reference(s): <br>
- [Course Builder Agent on ClawHub](https://clawhub.ai/freeman88-tch/course-builder-agent) <br>
- [Publisher profile](https://clawhub.ai/user/freeman88-tch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media files such as MP4 video, slide images, audio, and subtitles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local ffmpeg/ffprobe and edge-tts commands, install Python packages, write generated video files, and use optional digital-human services when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
