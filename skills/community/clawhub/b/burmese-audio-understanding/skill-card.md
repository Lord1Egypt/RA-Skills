## Description: <br>
High-accuracy Burmese audio transcription using Gemini 3.1 Flash Preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thelapyae](https://clawhub.ai/user/thelapyae) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users use this skill to transcribe Burmese voice notes or speech into Burmese text through a local Node.js command that uploads the selected audio to Google Gemini with their own API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio recordings are sent to Google Gemini for transcription. <br>
Mitigation: Use a scoped Gemini API key and avoid confidential or regulated recordings unless Google's handling terms fit the use case. <br>
Risk: Failed runs may not delete the uploaded remote file automatically. <br>
Mitigation: Review failed executions and remove uploaded files from the Gemini file service when cleanup does not complete. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thelapyae/burmese-audio-understanding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcription with setup and execution commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and an audio file path; the included script uploads audio as audio/ogg.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
