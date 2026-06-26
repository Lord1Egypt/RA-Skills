## Description: <br>
Process video and audio with correct codec selection, filtering, and encoding settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media engineers use this skill as a concise FFmpeg reference for selecting codecs, filters, stream mappings, seek behavior, audio settings, subtitles, concatenation, and hardware acceleration options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FFmpeg commands can overwrite or transform media files in ways that are difficult to reverse. <br>
Mitigation: Review generated commands before execution and write outputs to new filenames or backed-up directories. <br>
Risk: The skill depends on a locally installed ffmpeg binary whose safety and behavior depend on the installation source and version. <br>
Mitigation: Install ffmpeg from a trusted package source and keep it updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/ffmpeg) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown reference notes with inline FFmpeg command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ffmpeg binary; artifact metadata lists linux, darwin, and win32 support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
