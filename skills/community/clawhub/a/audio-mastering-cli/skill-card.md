## Description:

CLI audio mastering without a reference track using ffmpeg; accepts audio or video inputs and outputs mastered WAV/MP3 or remuxed MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alesys](https://clawhub.ai/user/alesys)

### License/Terms of Use:


## Use Case:

Developers and media creators use this skill to master audio or video inputs from the command line, producing mastered WAV/MP3 audio and remuxed MP4 video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact does not include scripts/master_media.ps1, while usage depends on running that PowerShell script from an unpinned GitHub clone.

Mitigation: Review the exact script from the repository before installing or running the skill, and prefer a pinned commit or signed release.

Risk: The skill creates mastered media files on disk and processes user-supplied input and output paths.

Mitigation: Confirm paths before execution and avoid running the PowerShell command in an elevated session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alesys/skills/audio-mastering-cli)
- [Project homepage](https://github.com/alesys/openclaw-skill-audio-mastering-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell commands and file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and PowerShell on Windows; creates mastered media files on disk.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
