## Description: <br>
Interactive AI avatar with Simli video rendering and ElevenLabs TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johannes-Berggren](https://clawhub.ai/user/Johannes-Berggren) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and operators use this skill to interact with an OpenClaw assistant through a browser-based avatar that speaks short conversational summaries, shows detailed markdown responses, and can forward configured Slack or email messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act as a high-trust local OpenClaw operator rather than only a visual or text-to-speech frontend. <br>
Mitigation: Deploy it only for trusted operator workflows and review the configured OpenClaw access before use. <br>
Risk: Slack, email, Stream Deck, kiosk mode, and broad business-tool prompts may expose or send sensitive information. <br>
Mitigation: Disable integrations that are not needed, use restricted API keys and Slack scopes, and avoid sensitive conversations unless external sharing is acceptable. <br>
Risk: External Simli and ElevenLabs services are required for avatar rendering and text-to-speech. <br>
Mitigation: Use service-specific restricted keys and confirm that the expected audio and avatar data sharing is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub Avatar Skill Page](https://clawhub.ai/Johannes-Berggren/avatar) <br>
- [Avatar README](artifact/README.md) <br>
- [Avatar Skill Definition](artifact/SKILL.md) <br>
- [Simli](https://simli.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, API calls] <br>
**Output Format:** [Plain spoken text plus markdown detail, with browser avatar rendering and optional configured Slack or email forwarding.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMLI_API_KEY and ELEVENLABS_API_KEY; optional Slack, OpenClaw, email, Stream Deck, and kiosk behavior depends on local configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
