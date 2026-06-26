## Description: <br>
Audio Note Taker transcribes audio recordings with OpenAI Whisper and saves structured notes for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who record meetings, lectures, interviews, work reviews, or quick voice notes can use this skill to turn audio into text notes. The generated notes should be reviewed before they are used as meeting minutes, summaries, or action-item records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected recordings are sent to OpenAI or a configured compatible provider for transcription. <br>
Mitigation: Use the skill only with recordings approved for external processing, avoid confidential or regulated audio unless approved, and use a limited API key where possible. <br>
Risk: Transcripts, speaker labels, summaries, action items, and advertised output formats may be incomplete or inaccurate. <br>
Mitigation: Manually verify generated notes before relying on them, especially for decisions, assignments, or published records. <br>
Risk: Generated notes are saved to a local output path chosen by the user or defaulted from the input filename. <br>
Mitigation: Choose an output location with appropriate access controls and review the file before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/audio-note-taker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json] <br>
**Output Format:** [Markdown notes by default, with text and JSON output options documented by the artifact.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY and an input audio file; writes notes to the selected local output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
