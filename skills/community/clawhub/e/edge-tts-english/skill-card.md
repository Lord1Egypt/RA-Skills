## Description: <br>
Generate high-quality English and multilingual audio using Microsoft Edge TTS, with American and British English voices, and return the resulting MP3 to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DavydenkovM](https://clawhub.ai/user/DavydenkovM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn provided text into spoken audio for pronunciation practice, read-aloud requests, and language learning, then return the generated MP3. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text provided for speech synthesis is sent to Microsoft Edge TTS through the edge-tts client. <br>
Mitigation: Do not use the skill for passwords, secrets, private messages, or confidential documents. <br>
Risk: The skill depends on an installed edge-tts binary and writes generated audio files to local output paths. <br>
Mitigation: Verify the edge-tts binary comes from a trusted source and keep generated MP3 files in temporary or intended output locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DavydenkovM/edge-tts-english) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files] <br>
**Output Format:** [MP3 audio file path and generated MP3 media] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a selectable Microsoft Edge TTS voice and writes the audio to a temporary or caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
