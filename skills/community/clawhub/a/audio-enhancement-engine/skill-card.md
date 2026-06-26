## Description: <br>
Audio Enhancement Engine helps agents run local audio enhancement and repair for audio files or folders using VoiceFixer for speech restoration and AudioSR for 48 kHz high-fidelity super-resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and audio workflows use this skill to enhance speech recordings, meetings, podcasts, music, and batches of common audio formats locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First run can download dependencies or model code and change the Python environment. <br>
Mitigation: Run in an isolated container or disposable virtual environment, and review and pin dependency sources before use. <br>
Risk: Recursive batch mode can process more local audio files than intended. <br>
Mitigation: Point the skill only at audio files or folders explicitly intended for enhancement and review output paths before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/audio-enhancement-engine) <br>
- [AudioSR](https://github.com/haoheliu/versatile_audio_super_resolution.git) <br>
- [VoiceFixer](https://github.com/haoheliu/voicefixer.git) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Enhanced audio is written as WAV; VoiceFixer uses an _enhanced suffix and AudioSR produces 48 kHz output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
