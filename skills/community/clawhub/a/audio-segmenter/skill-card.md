## Description:

Audio-Segmenter helps agents split a single audio file or a folder of audio files into fixed-duration segments while preserving the source folder structure and choosing default output paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare speech datasets, karaoke material, cover-song assets, podcasts, or other long audio by slicing inputs into smaller fixed-duration files. The skill supports a required input path plus optional duration, output directory, and recursive folder processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs Python packages and downloads FFmpeg, which can change the user's Python environment.

Mitigation: Review before installing, run in an isolated sandbox or disposable virtual environment, and require pinned dependencies plus verified FFmpeg binaries before using it on sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/audio-segmenter)
- [Python documentation](https://www.python.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated audio segment files are written to the selected output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python. The artifact may create or update a virtual environment and download FFmpeg before processing audio.]

## Skill Version(s):

1.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
