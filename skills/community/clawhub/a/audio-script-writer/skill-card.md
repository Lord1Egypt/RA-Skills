## Description: <br>
Convert written medical content into podcast or video scripts optimized for audio delivery, including pronunciation notes, timing metadata, and audio-friendly structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical educators, content producers, and developers use this skill to convert written medical or scientific material into spoken-word scripts for podcasts, videos, lectures, audiobooks, and patient education. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential or regulated medical content could be supplied as input. <br>
Mitigation: Avoid processing patient or confidential medical data unless permitted, and review input and output paths before running the skill. <br>
Risk: Generated scripts may preserve inaccurate, outdated, or incomplete medical claims from the source material. <br>
Mitigation: Have qualified reviewers verify medical accuracy, audience suitability, and final narration copy before publication or recording. <br>
Risk: The provided requirements file lists standard-library modules as dependencies, which can lead to unnecessary dependency installation attempts. <br>
Mitigation: Run the script with the Python standard library and do not install packages from the requirements file unless separately reviewed. <br>


## Reference(s): <br>
- [Audio Script Writer References](artifact/references/guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [JSON containing an audio script, metadata, pronunciation notes, and formatting cues; optionally written to an output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates duration from selected pace and target duration, expands common abbreviations, converts small numbers to words, and uses only Python standard-library behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
