## Description:

Process video and audio with correct codec selection, filtering, and encoding settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and media engineers use this skill to ask an agent for FFmpeg command guidance covering seeking, stream selection, encoding, filters, subtitles, concatenation, audio handling, and hardware acceleration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FFmpeg commands may read media files, write output files, or overwrite existing outputs when run.

Mitigation: Review generated commands, paths, and output names before execution, especially when processing untrusted media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/ffmpeg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline FFmpeg command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ffmpeg binary on linux, darwin, or win32 when generated commands are executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
