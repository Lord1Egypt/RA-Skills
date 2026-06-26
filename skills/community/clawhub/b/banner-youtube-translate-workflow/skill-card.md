## Description: <br>
Automates downloading YouTube audio, launching Doubao, playing audio, and capturing translations for full video subtitle extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banner90](https://clawhub.ai/user/banner90) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Users who need full-video translation use this skill to download YouTube audio, launch Doubao, play the audio through a visible Windows desktop, and capture translated subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs an external absolute-path Python script that is not included in the artifact for review. <br>
Mitigation: Install only after inspecting and trusting the external workflow.py script and the helper skills it chains. <br>
Risk: The workflow downloads YouTube audio, plays audio, and saves audio and transcript files locally. <br>
Mitigation: Avoid private or sensitive videos unless local processing, playback, and file retention are acceptable. <br>
Risk: The workflow depends on visible Windows desktop automation for Doubao. <br>
Mitigation: Run it only in a controlled desktop session where GUI access, accounts, and output directories are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banner90/banner-youtube-translate-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and a JSON result schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audio and translation files; requires Windows GUI automation with a visible desktop.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
