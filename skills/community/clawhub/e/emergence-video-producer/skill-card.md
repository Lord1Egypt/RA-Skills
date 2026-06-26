## Description: <br>
Automated video production pipeline for product demos and academic tutorials using WebReel for browser recording, DashScope or Edge-TTS for narration, and FFmpeg for assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and product teams use this skill to turn an approved Markdown video script or storyboard into a browser walkthrough or slide-style tutorial video with generated narration and assembled media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated storyboards, target URLs, narration text, and recording configuration may not match the user's intent or could expose unintended content. <br>
Mitigation: Require human review and approval of the storyboard, generated configuration, target URL, and narration text before production. <br>
Risk: External tools such as WebReel, FFmpeg, Edge-TTS, DashScope, and Pillow must be trusted and correctly configured before execution. <br>
Mitigation: Install only trusted local toolchains and credentials, and run production in a controlled environment with the required dependencies available. <br>
Risk: Generated audio, frame, and video outputs can overwrite files or leave intermediate artifacts in shared directories. <br>
Mitigation: Use a dedicated output directory and review output paths before running recording or assembly steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/emergence-video-producer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown storyboards, JSON configuration, generated audio/video files, and shell commands for recording and assembly] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intermediate storyboard, Slidev or WebReel configuration, narration audio, extracted frames, and final MP4 output when required tools are available.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
