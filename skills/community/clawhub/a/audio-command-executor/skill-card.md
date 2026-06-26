## Description: <br>
Processes inbound audio files, transcribes them, and answers to resulting texts. Converts non-WAV inputs to WAV before transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirkovz](https://clawhub.ai/user/sirkovz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to process inbound audio files, convert them to WAV when needed, transcribe German speech, and handle the resulting text as a normal chat request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local audio conversion and transcription tools on inbound file paths. <br>
Mitigation: Install only for trusted inbound audio directories, validate that paths remain inside the expected directory, and use safe argv-style command execution. <br>
Risk: Audio-derived instructions are treated like normal chat requests and could include sensitive or unintended commands. <br>
Mitigation: Ask for confirmation before acting on sensitive spoken instructions and restrict expected audio file types before processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sirkovz/audio-command-executor) <br>
- [Publisher profile](https://clawhub.ai/user/sirkovz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [German natural-language response with error messages when audio conversion or transcription fails] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local ffmpeg and whisper.cpp commands against an inbound audio file path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
