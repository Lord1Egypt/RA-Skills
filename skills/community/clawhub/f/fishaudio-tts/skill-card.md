## Description: <br>
Text-to-Speech using FishAudio (fish.audio), generates natural human-like voice with great emotional expression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iZorro](https://clawhub.ai/user/iZorro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to convert supplied text into FishAudio-generated MP3 speech with selectable voice options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to FishAudio. <br>
Mitigation: Only synthesize text that is appropriate to send to the FishAudio service. <br>
Risk: The script can read API-key material from a broad TOOLS.md file and writes MP3 output to the requested path. <br>
Mitigation: Prefer --api-key or FISH_AUDIO_API_KEY for secrets, and choose output paths deliberately before running the command. <br>


## Reference(s): <br>
- [FishAudio](https://fish.audio/) <br>
- [ClawHub release page](https://clawhub.ai/iZorro/fishaudio-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [MP3 audio file with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FishAudio API key and writes generated audio to a user-selected local path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
