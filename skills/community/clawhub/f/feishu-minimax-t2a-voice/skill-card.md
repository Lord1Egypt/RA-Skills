## Description: <br>
Generates Feishu voice replies from text using MiniMax T2A with Edge TTS fallback, then returns an audio file path for sending as audio/opus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michelangelo-in-sistine](https://clawhub.ai/user/michelangelo-in-sistine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn Feishu reply text into a voice message workflow, generating an audio file through MiniMax T2A when configured or Edge TTS as a fallback. It is useful when a Feishu conversation should be answered with synthesized voice instead of plain text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice-reply text may be sent to MiniMax or Edge TTS services. <br>
Mitigation: Avoid secrets or highly sensitive content, and use a dedicated MiniMax API key when MiniMax is configured. <br>
Risk: Generated audio can remain in the configured media output directory until overwritten or cleaned up. <br>
Mitigation: Restrict access to the media output directory and clean generated audio files according to local retention needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michelangelo-in-sistine/feishu-minimax-t2a-voice) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Text with inline shell commands, file paths, and Feishu message parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces .opus or .ogg audio files when synthesis succeeds and falls back to text when audio generation fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
