## Description: <br>
Helps agents analyze, convert, compress, edit, stream, and validate audio or video files with ffmpeg and ffprobe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunalshah](https://clawhub.ai/user/kunalshah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media engineers, and content operators use this skill to generate ffmpeg and ffprobe workflows for media conversion, editing, analysis, streaming, repair, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ffmpeg commands may capture screens, cameras, microphones, streams, or rolling DVR windows without enough privacy, consent, destination, or retention guardrails. <br>
Mitigation: Review commands before running them, confirm devices and screen regions, use capture or streaming only with consent, and verify destination URLs, audience settings, and retention windows. <br>
Risk: Streaming and restreaming workflows can expose stream keys or private destinations through chat, logs, or shell history. <br>
Mitigation: Avoid pasting real stream keys into prompts or logs; use environment variables or local secret handling where possible. <br>


## Reference(s): <br>
- [ffprobe Analysis Reference](references/ffprobe-analysis.md) <br>
- [Codec & Container Compatibility Matrix](references/codecs-containers.md) <br>
- [FFmpeg Flag Reference](references/ffmpeg-flags.md) <br>
- [Audio-Video Skill Feature Overview](assets/features.md) <br>
- [Platform-Specific Encoding Presets](assets/platform-presets.md) <br>
- [Audio/Video Output Quality Checklist](assets/quality-checklist.md) <br>
- [Homebrew FFmpeg Formula](https://formulae.brew.sh/formula/ffmpeg) <br>
- [John Van Sickle FFmpeg Static Builds](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz) <br>
- [Gyan FFmpeg Windows Builds](https://www.gyan.dev/ffmpeg/builds/) <br>
- [Google Spatial Media](https://github.com/google/spatial-media) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands should be reviewed before execution, especially for capture, streaming, restreaming, and DVR workflows.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
