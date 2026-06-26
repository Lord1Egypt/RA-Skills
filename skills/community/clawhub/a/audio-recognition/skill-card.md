## Description: <br>
Audio Recognition helps agents transcribe uploaded audio into text, identify speech-related details such as keywords or song titles, and prepare outputs such as meeting notes, subtitles, or searchable transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzhimin](https://clawhub.ai/user/zzhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to convert meeting recordings, media files, voice commands, or other uploaded audio into transcript text with optional speaker labels and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio may be uploaded to an external transcription engine or provider depending on deployment choices. <br>
Mitigation: Confirm the selected transcription engine and data handling path before installation, and treat the privacy statement as policy guidance rather than technical enforcement. <br>
Risk: Transcripts may be inaccurate for noisy recordings, heavy accents, dialects, or unsupported languages. <br>
Mitigation: Review generated transcripts before relying on them for decisions, publication, or records. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text transcript with optional speaker labels and timestamps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accuracy depends on audio quality, background noise, accent, language coverage, and the transcription engine selected by the deploying agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
