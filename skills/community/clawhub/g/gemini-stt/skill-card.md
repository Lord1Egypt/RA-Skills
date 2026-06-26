## Description: <br>
Transcribe audio files using Google's Gemini API or Vertex AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to convert local audio files, including voice-message recordings, into plain text transcripts through Google Gemini or Vertex AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Google Gemini or Vertex AI for transcription. <br>
Mitigation: Use the skill only when organizational policy permits cloud processing of the recording content. <br>
Risk: The transcription runs under the configured Gemini API key or Google Cloud Application Default Credentials. <br>
Mitigation: Confirm the intended account, project, and region before processing sensitive or customer-provided audio. <br>
Risk: Confidential, regulated, or third-party recordings may require additional approval before external processing. <br>
Mitigation: Avoid those recordings unless the applicable policy and consent requirements allow use of Google transcription services. <br>


## Reference(s): <br>
- [Gemini API Models](https://ai.google.dev/gemini-api/docs/models) <br>
- [ClawHub skill page](https://clawhub.ai/araa47/gemini-stt) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/araa47) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text transcript with command-line usage and authentication configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads supported audio files and returns only the transcription text when the API call succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
