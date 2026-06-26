## Description: <br>
Command-line guidance for using Deepgram's CLI to transcribe local files, URLs, microphone input, and piped audio with configurable speech-to-text options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerkn](https://clawhub.ai/user/nerkn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate the Deepgram CLI for speech-to-text transcription from files, URLs, live microphone input, or STDIN. It supports scripting workflows that capture transcripts as JSON, text, subtitles, or other CLI-supported formats for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Deepgram CLI uses a locally stored API key. <br>
Mitigation: Protect the API key, avoid committing it to source control, and rotate it if exposure is suspected. <br>
Risk: Audio submitted for transcription may contain confidential, personal, or regulated information. <br>
Mitigation: Transcribe only audio the user is authorized to send to Deepgram and review applicable data-handling requirements before use. <br>
Risk: Installing the wrong package could expose credentials or audio data. <br>
Mitigation: Verify that @deepgram/cli is the official package before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerkn/deepgram) <br>
- [Publisher profile](https://clawhub.ai/user/nerkn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript output depends on Deepgram CLI flags and may include JSON, text, SRT, or VTT.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
