## Description: <br>
Creates videos from text by guiding an agent through storyboard planning, image generation, voiceover creation, and MP4 assembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn product, education, brand, or social-media prompts into storyboarded videos with generated frames, narration, and ffmpeg assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, scripts, narration, and generated media may be sent to SiliconFlow through dependent skills. <br>
Mitigation: Avoid private or business-sensitive inputs unless that external processing is acceptable, and review china-image-gen and china-tts separately before deployment. <br>
Risk: The workflow requires a sensitive SiliconFlow API key and can incur API usage costs. <br>
Mitigation: Use a limited or monitored API key, keep the key out of shared logs and files, and monitor usage during generation. <br>
Risk: Generated media is saved locally and may contain sensitive or unapproved content. <br>
Mitigation: Review generated assets before sharing and delete local frames, audio, and video files that contain private or business-sensitive material. <br>
Risk: Video assembly depends on locally installed ffmpeg. <br>
Mitigation: Install ffmpeg only from trusted sources and keep the local toolchain patched. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tobewin/china-video-gen) <br>
- [Dependency guide](references/dependencies.md) <br>
- [ffmpeg synthesis parameters](references/ffmpeg.md) <br>
- [Storyboard design guide](references/storyboard.md) <br>
- [china-image-gen dependency](https://clawhub.ai/ToBeWin/china-image-gen) <br>
- [china-tts dependency](https://clawhub.ai/ToBeWin/china-tts) <br>
- [ffmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with storyboard sections, prompts, command snippets, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to create local frames, voiceover audio, and a final MP4 video file.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
