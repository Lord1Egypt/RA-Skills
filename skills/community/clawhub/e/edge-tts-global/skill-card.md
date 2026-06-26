## Description: <br>
Use the globally installed edge-tts command to generate Chinese or multilingual text-to-speech audio on this machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text into Chinese or multilingual speech with the globally installed edge-tts command, optionally producing Telegram voice-message style audio and subtitles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup can delete files outside the intended temporary audio workflow. <br>
Mitigation: Limit execution to agents with constrained filesystem access or change cleanup to delete only files created under the workspace temp/ directory. <br>
Risk: The workflow depends on a globally installed edge-tts binary and sends text to the TTS provider used by that binary. <br>
Mitigation: Confirm the installed binary is trusted and that the text being synthesized is appropriate to send to the provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrliugangqiang/edge-tts-global) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP3 audio files, optional VTT subtitles, and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a globally installed edge-tts binary and writes temporary outputs under the caller workspace temp/ directory by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
