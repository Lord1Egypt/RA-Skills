## Description: <br>
Automatically turns stories into stylized animated videos with selectable generation modes, voiceover, burned-in subtitles, and BGM selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn a story into a short animated video workflow, including scene planning, style selection, voiceover, subtitles, BGM selection, and final MP4 assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story text, prompts, and generated media requests may be sent to Doubao/Volcengine and TTS services. <br>
Mitigation: Use a limited API key, avoid sensitive story material, and confirm external-service handling before running the workflow. <br>
Risk: The workflow downloads and processes generated media locally and may write into configured output and resource folders. <br>
Mitigation: Run it in a dedicated output directory and avoid placing unrelated private files under the configured media resource paths. <br>
Risk: The workflow depends on local media tooling and bundled paths that may not match every environment. <br>
Mitigation: Review the doubao-media dependency, ffmpeg/Pillow setup, and hard-coded Windows resource paths before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/systiger/ai-animation-choose) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [BGM_LIBRARY.md](artifact/BGM_LIBRARY.md) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with command examples, configuration details, and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local images, audio, subtitle-burned MP4 video, and final H.264/AAC MP4 output when executed with the required services and media tools.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
