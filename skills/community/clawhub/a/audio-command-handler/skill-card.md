## Description: <br>
Handle audio messages as commands by transcribing WAV, PCM, or MP3 audio with iFlytek Speed Transcription, then either executing the transcription as the command or using it as context for an accompanying text command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn user-supplied audio messages into agent instructions, or to use transcribed audio as context for a separate text command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken or transcribed content can become actionable agent instructions without enough user control. <br>
Mitigation: Show the transcript and require user confirmation before executing commands, writing files, or uploading generated content. <br>
Risk: Audio may contain private, regulated, or secret-bearing content that is sent to transcription or upload services. <br>
Mitigation: Use only with trusted transcription and upload services, and avoid processing sensitive audio unless the user has explicitly accepted that data handling. <br>
Risk: Long audio-plus-text results can be saved and uploaded automatically. <br>
Mitigation: Require explicit consent before uploading generated files and provide the destination URL to the user after upload. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Plain text or JSON from the helper script, with optional generated HTML files and uploaded result URLs for longer outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports WAV, PCM, and MP3 inputs; audio-only mode treats the transcript as the command, while audio-plus-text mode treats the transcript as context.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
