## Description: <br>
Auto video production, TTS voiceover, media management, batch export | AI 自动成片、TTS 配音、素材管理、批量导出. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lasbder-ops](https://clawhub.ai/user/lasbder-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Video creators, editors, and automation developers use this skill to collect stock footage, generate voiceover, assemble videos, create subtitles, normalize audio, and assist Final Cut Pro workflows from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scripts may write or overwrite generated media files in the selected project folders. <br>
Mitigation: Review output paths before running or rerunning scripts, and keep project outputs in a dedicated working directory. <br>
Risk: Narration text and media paths may be sent to local Qwen TTS or ASR services. <br>
Mitigation: Use trusted local services only and avoid passing sensitive scripts or media unless the local service is approved for that content. <br>
Risk: The media collector downloads stock footage from external services. <br>
Mitigation: Use trusted API keys and review downloaded media metadata and licensing before publication. <br>


## Reference(s): <br>
- [FCP Assistant on ClawHub](https://clawhub.ai/lasbder-ops/fcp-assistant) <br>
- [lasbder-ops ClawHub profile](https://clawhub.ai/user/lasbder-ops) <br>
- [Pexels API](https://www.pexels.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide scripts that create or overwrite local media files, metadata, subtitles, thumbnails, and audio/video outputs.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
