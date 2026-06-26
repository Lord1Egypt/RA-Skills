## Description: <br>
Transcribes audio messages, voice notes, and recordings into text in 50+ languages using Groq's Whisper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huixionghexiyi](https://clawhub.ai/user/huixionghexiyi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and users who need voice-to-text transcription can use this skill to configure Groq access and transcribe individual or folder-based audio files for messages, meetings, accessibility workflows, and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to Groq for transcription. <br>
Mitigation: Use the skill only with audio you are authorized to send to Groq, and avoid confidential meetings or sensitive voice notes unless consent and policy allow it. <br>
Risk: The setup guidance places a Groq API key in local configuration. <br>
Mitigation: Keep the API key out of version control and shared documents, prefer environment variables where possible, and rotate the key if it is exposed. <br>
Risk: Folder-wide transcription can upload more audio than intended. <br>
Mitigation: Review the target folder and file list before batch transcription, and limit runs to files intended for external transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huixionghexiyi/free-groq-voice) <br>
- [Groq Console](https://console.groq.com/) <br>
- [Groq audio transcription API endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription output with Markdown setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Groq API key and may use an HTTP proxy in restricted regions.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/_meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
