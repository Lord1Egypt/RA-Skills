## Description: <br>
Create and manage voices, speech synthesis, audio projects, and conversational AI agents in ElevenLabs via the ElevenLabs API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an ElevenLabs account through ClawLink, discover available ElevenLabs tools, and perform voice, speech, project, dubbing, and conversational agent workflows from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects OpenClaw to a third-party ClawLink plugin and an ElevenLabs account using sensitive API credentials. <br>
Mitigation: Proceed only when the user trusts ClawLink to broker the credentials, and keep API keys out of chat because ClawLink manages authentication. <br>
Risk: Write operations can create, update, delete, or modify ElevenLabs voices, history items, projects, dubbing jobs, pronunciation dictionaries, and conversational agents. <br>
Mitigation: Preview and explicitly confirm write or destructive actions before execution, including the target resource and intended effect. <br>
Risk: ConvAI agent configuration and knowledge base changes may expose or alter sensitive business logic. <br>
Mitigation: Review requested agent prompts, knowledge sources, and configuration changes before calling write tools. <br>


## Reference(s): <br>
- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference/overview) <br>
- [ElevenLabs API Reference](https://elevenlabs.io/docs/api-reference) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/elevenlabs-audio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or retrieve audio-related outputs through ElevenLabs and ClawLink tools when the connected account and selected operation support them.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
