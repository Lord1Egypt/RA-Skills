## Description: <br>
Downloads YouTube audio, launches Doubao, plays the audio, and captures translated subtitles as part of a YouTube video translation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation users use this skill to translate YouTube video audio through a Windows/WSL workflow that coordinates audio download, Doubao launch, playback, and subtitle capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow downloads media and stores generated audio and translation files locally. <br>
Mitigation: Use a dedicated workspace, review saved file locations, and delete generated media and translation files when they are no longer needed. <br>
Risk: The workflow controls a visible Doubao desktop session and may play audio over speakers. <br>
Mitigation: Run it only in an appropriate desktop session, avoid sensitive audio or private on-screen content, and do not disconnect the visible desktop during GUI automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banner90/byt-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [JSON result with local file paths and duration metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local audio and translation files in a Windows works directory and requires a visible Windows desktop session for GUI automation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact package files report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
