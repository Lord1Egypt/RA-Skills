## Description: <br>
Automates local video-editing workflows from media analysis through clipping, subtitles, effects, audio processing, and final export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai285384076-droid](https://clawhub.ai/user/ai285384076-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, editors, and developers use this skill to process local video, audio, and image folders and generate edited videos such as highlights, short videos, explainers, and vlogs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python and FFmpeg media-processing tools over user-selected folders. <br>
Mitigation: Use a virtual environment, point the skill only at intended media folders, and review command inputs before execution. <br>
Risk: Generated videos and intermediate files may overwrite or expose sensitive media if output locations are chosen carelessly. <br>
Mitigation: Use a dedicated output directory, avoid sensitive or cloud-synced folders unless intended, keep backups, and review outputs before sharing. <br>


## Reference(s): <br>
- [Quickstart Guide](references/quickstart.md) <br>
- [Default Configuration](references/default_config.yaml) <br>
- [FFmpeg Command Reference](references/ffmpeg_guide.md) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local Python and FFmpeg media-processing scripts that read selected media folders and write generated video outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
