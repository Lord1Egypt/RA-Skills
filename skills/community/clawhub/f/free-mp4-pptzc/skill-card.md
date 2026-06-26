## Description: <br>
Helps create narrated MP4 presentation videos from text scripts or slide-style content using generated slide images, optional HTML templates, Edge TTS narration, and ffmpeg composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users can use this skill to turn presentation scripts into slide images, narration audio, and final MP4 presentation videos for reports, demos, training, or tutorials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Narration text may be sent to Edge TTS. <br>
Mitigation: Avoid confidential scripts unless external TTS use is approved, and review or redact narration text before generating audio. <br>
Risk: HTML rendering may install Playwright and browser binaries on the host. <br>
Mitigation: Run the skill in an isolated environment and approve dependency and browser downloads before execution. <br>
Risk: Video generation can overwrite output files. <br>
Mitigation: Use a dedicated output directory and verify output paths before running synthesis commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/openclawzhangchong/free-mp4-pptzc) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP4 video files, PNG slide images, MP3 narration, and Markdown instructions with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install browser tooling for HTML rendering and uses ffmpeg for video synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
