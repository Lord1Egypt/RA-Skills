## Description: <br>
Accept text or voice input, transcribe if needed, generate natural OpenAI TTS speech, and send audio output to Feishu chat or web player. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengzhuowen](https://clawhub.ai/user/pengzhuowen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or share a reusable Feishu voice workflow that accepts text or local audio, optionally transcribes voice input, synthesizes OpenAI speech, and returns audio to Feishu or a web player. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a locally configured transcription command from the user's OpenClaw configuration. <br>
Mitigation: Review the configured audio command in ~/.openclaw/openclaw.json before use and keep that configuration protected. <br>
Risk: Text and voice-derived content may be sent to OpenAI and Feishu services. <br>
Mitigation: Avoid regulated, secret, or highly sensitive content unless the data-flow policy is acceptable for the deployment. <br>
Risk: The security verdict is suspicious because consent boundaries for third-party processing are not clearly documented. <br>
Mitigation: Confirm user consent and service data-handling requirements before deploying the workflow. <br>


## Reference(s): <br>
- [Input / Output Workflow](references/input-output-workflow.md) <br>
- [Feishu Voice Loop Presets](references/presets.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/pengzhuowen/feishu-voice-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate temporary WAV and OGG audio files during execution; the transcription helper emits JSON containing transcript text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
