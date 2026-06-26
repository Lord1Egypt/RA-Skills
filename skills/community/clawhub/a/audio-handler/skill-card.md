## Description: <br>
Audio Handler helps agents read, analyze, convert, and process local audio files across common formats including MP3, WAV, FLAC, AAC, M4A, OGG, OPUS, WMA, and AIFF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and automation agents use this skill to inspect local audio metadata and run audio-processing workflows for conversion, trimming, normalization, merging, extraction, playback, and text-to-speech tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion, trimming, and normalization workflows can overwrite selected output files. <br>
Mitigation: Review commands before execution and choose fresh output filenames or keep backups before running the audio-processing scripts. <br>
Risk: The skill depends on local ffmpeg, ffprobe, and jq installations for processing and metadata extraction. <br>
Mitigation: Use trusted local installations of these tools and verify command output before relying on processed audio files. <br>


## Reference(s): <br>
- [Audio Handler Skill Documentation](artifact/SKILL.md) <br>
- [Audio Handler on ClawHub](https://clawhub.ai/Neckr0ik/audio-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands and local command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local audio tools such as ffmpeg, ffprobe, and jq; macOS playback and text-to-speech examples use afplay and say.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
