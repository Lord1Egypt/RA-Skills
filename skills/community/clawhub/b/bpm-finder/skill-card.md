## Description: <br>
Use this skill when the user needs BPM finder help inside Codex, including tap tempo estimation, BPM conversion, tempo normalization, lightweight tempo analysis workflows, or guidance on when to use the full BPM Finder website for browser-based audio analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsgtcyx](https://clawhub.ai/user/wsgtcyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to estimate BPM from tap intervals, timestamps, or explicit local audio files, convert between BPM and milliseconds, and decide when a browser-based BPM Finder workflow is a better fit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio-file analysis reads local files and invokes ffmpeg on user-provided paths. <br>
Mitigation: Only analyze audio files the user explicitly provides and use a trusted local ffmpeg installation. <br>
Risk: Tempo detection can produce approximate, half-time, or double-time readings. <br>
Mitigation: Report the input source, confidence when available, and any plausible half-time or double-time interpretation. <br>


## Reference(s): <br>
- [BPM Finder website](https://bpm-finder.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise numeric results and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BPM, confidence, intervals, duration, and half-time or double-time notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
