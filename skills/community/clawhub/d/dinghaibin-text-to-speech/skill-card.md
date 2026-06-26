## Description: <br>
Convert text to speech audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text into speech audio files for voiceovers, podcasts, article narration, and multilingual audio generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text may be sent to the gTTS external provider when that backend is used. <br>
Mitigation: Avoid confidential input unless the user accepts the external provider boundary. <br>
Risk: The output file path is user-controlled. <br>
Mitigation: Review the requested output path before running the command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/dinghaibin-text-to-speech) <br>
- [Publisher Profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with command examples and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an audio file at the requested output path when the local text-to-speech backend is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
