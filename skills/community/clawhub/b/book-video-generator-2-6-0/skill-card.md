## Description:

Generates a three-minute book explainer video from a book title and author, covering review copy, AI illustrations, TTS narration, subtitles, and MP4 composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjun198711](https://clawhub.ai/user/chenjun198711)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate short Chinese book-review videos by guiding an agent through research, scriptwriting, storyboard generation, image creation, TTS narration, subtitle timing, cover creation, and final MP4 composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party search, image generation, and TTS services may receive book titles, prompts, and narration text.

Mitigation: Use trusted providers, avoid sensitive inputs, and confirm data handling terms before generation.

Risk: The skill may install unpinned Python packages automatically.

Mitigation: Install dependencies manually in an isolated virtual environment and pin versions before production use.

Risk: Persistent agent setup steps may modify local agent configuration.

Mitigation: Review configuration changes, including any ~/.codex/config.toml edits, before applying them.

Risk: A local Stable Diffusion WebUI endpoint can execute generation requests against whatever service SD_WEBUI_URL points to.

Mitigation: Set SD_WEBUI_URL only to a trusted local endpoint.

Risk: The original workflow reference may contain hard-coded user attribution.

Mitigation: Remove hard-coded user_id attribution before reusing or adapting that workflow.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/chenjun198711/skills/book-video-generator-2-6-0)
- [Prompt Reference](artifact/references/prompts.md)
- [Cross-Platform Guide](artifact/references/CROSS_PLATFORM.md)
- [Original Workflow Reference](artifact/references/workflow-original.yaml)
- [Demo Page](https://chenjun198711.github.io/book-video-generator/)
- [Agent Skills Open Standard](https://agentskills.io)
- [Volcengine Speech Console](https://console.volcengine.com/speech/new)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON structures, shell commands, generated images, MP3 audio, subtitles, and MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final media depends on user-provided book metadata, search results, selected image generation backend, selected TTS engine, and local ffmpeg composition.]

## Skill Version(s):

2.6.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
