## Description:

Transcribes a video's audio with word-level timings, translates the subtitles, burns them into the video, and can add a timing-fitted dub track when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

People who need to localize a video can use this skill to create translated subtitles and a subtitled MP4, with optional voice dubbing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses ffmpeg overwrite mode, which can replace existing files with matching output names.

Mitigation: Check for filename conflicts and use a working directory with backups before processing.

Risk: Video and audio files are uploaded to dLazy services for processing, and authentication can save an API key in local CLI configuration.

Mitigation: Confirm the media is appropriate to send to the service, and protect or rotate saved API credentials.

Risk: The documented translation prompt is fixed to Simplified Chinese.

Mitigation: Confirm that Simplified Chinese is the intended subtitle language before running the translation step.

## Reference(s):

- [CLI project page (skill metadata link)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)
- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-video-translate)

## Skill Output:

**Output Type(s):** [Video files, Subtitle files]

**Output Format:** [MP4 video and SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Subtitles are burned into the video; fitted dubbing is added only when requested.]

## Skill Version(s):

1.0.33 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
