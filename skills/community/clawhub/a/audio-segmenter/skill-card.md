## Description: <br>
Segments audio files or folders into fixed-duration clips with optional recursive folder processing while preserving the input folder structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and dataset preparers use this skill to split long audio files or audio folders into shorter fixed-duration clips for speech datasets, karaoke material, cover-song preparation, or media organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or modify a Python environment, install packages, download ffmpeg, write logs, and generate many output audio files. <br>
Mitigation: Run it in an isolated environment, preinstall verified dependencies where possible, and confirm input, output, and recursive-processing paths before execution. <br>
Risk: Automatic dependency and ffmpeg downloads occur without a clear consent boundary. <br>
Mitigation: Review the dependency installation behavior before use and restrict network access or pre-provision dependencies in managed environments. <br>


## Reference(s): <br>
- [Audio-Segmenter ClawHub page](https://clawhub.ai/wangminrui2022/audio-segmenter) <br>
- [Publisher profile](https://clawhub.ai/user/wangminrui2022) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and generated audio segment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs fixed-duration audio clips and may create output directories, logs, a Python environment, and downloaded ffmpeg dependencies.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
