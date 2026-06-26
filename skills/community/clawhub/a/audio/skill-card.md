## Description: <br>
Process, enhance, and convert audio files with noise removal, normalization, format conversion, transcription, and podcast workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and production teams use this skill to inspect, convert, clean, normalize, transcribe, and package user-provided audio files with FFmpeg-centered workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audio commands can overwrite, transform, or concatenate the wrong files if paths and generated file lists are not reviewed. <br>
Mitigation: Work in a dedicated folder, keep backups of source recordings, and review generated commands and concat lists before running them. <br>
Risk: Cloud transcription examples may expose sensitive recordings or metadata to third-party providers. <br>
Mitigation: Use local transcription where appropriate, and only send recordings to cloud services after confirming approval and provider privacy and retention terms. <br>
Risk: Example API-token placeholders could lead users to paste secrets into shared commands or files. <br>
Mitigation: Use environment variables or approved secret-handling mechanisms for real tokens. <br>


## Reference(s): <br>
- [ClawHub Audio release page](https://clawhub.ai/ivangdavila/audio) <br>
- [FFmpeg audio commands](commands.md) <br>
- [Loudness standards by platform](loudness.md) <br>
- [Podcast production workflow](podcast.md) <br>
- [Transcription workflow](transcription.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and workflow checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audio-processing instructions; generated commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
