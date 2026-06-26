## Description: <br>
CLI audio mastering without a reference track using ffmpeg; accepts audio or video inputs and outputs mastered WAV/MP3 or remuxed MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alesys](https://clawhub.ai/user/alesys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media operators use this skill to ask an agent to master audio or video files locally through a repeatable ffmpeg and PowerShell workflow. It is intended for audio/video inputs that need conservative loudness normalization, compression, limiting, and exported mastered files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package asks the agent to run a local PowerShell script that was not included in the reviewed artifact. <br>
Mitigation: Install and use only after obtaining scripts/master_media.ps1 from a trusted source and reviewing it before execution. <br>
Risk: The workflow runs local PowerShell and ffmpeg commands against user-supplied media file paths. <br>
Mitigation: Use trusted input files, avoid unusual or untrusted paths, and confirm command arguments before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alesys/audio-mastering-cli) <br>
- [Project homepage](https://github.com/alesys/openclaw-skill-audio-mastering-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands, file paths, and mastering result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local creation of mastered WAV, optional MP3, and remuxed MP4 output files.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
