## Description: <br>
Converts Chinese text or text files into MP3 audio using Microsoft Edge neural text-to-speech voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate Chinese narration, announcements, story readings, or other spoken audio from provided text or a selected text file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text may be sent to the Edge TTS service for speech generation. <br>
Mitigation: Do not use confidential or sensitive text unless the service use is approved for that content. <br>
Risk: The skill depends on the edge_tts Python package. <br>
Mitigation: Install edge_tts only from a trusted package source and review dependency provenance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/effeceee/edge-tts-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an MP3 file at the requested output path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
