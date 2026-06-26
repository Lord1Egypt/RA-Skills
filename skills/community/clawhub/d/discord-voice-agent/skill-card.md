## Description: <br>
Use when building, configuring, running, debugging, or extending a Discord voice agent integrated with OpenClaw, including first-time setup, voice capture, transcription, TTS, slash commands, reply routing, health/status, and release work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsvips](https://clawhub.ai/user/itsvips) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, test, troubleshoot, and extend an OpenClaw-backed Discord voice bot that joins voice channels, captures speech, routes replies, and speaks back concise responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord tokens and OpenClaw gateway tokens can be exposed through chats, logs, screenshots, or committed files. <br>
Mitigation: Store tokens in environment variables or a secret manager, avoid sharing them in plaintext, and rotate credentials if exposure is suspected. <br>
Risk: Voice capture, transcription, OpenClaw routing, and local history may contain participant speech or sensitive conversation content. <br>
Mitigation: Run the bot only in channels where participants understand how voice is captured and routed, and define retention and deletion practices for `.kittu-voice-history/` and `.kittu-voice-captures/`. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/itsvips/discord-voice-agent) <br>
- [Quickstart](references/quickstart.md) <br>
- [First-run Wizard Flow](references/wizard.md) <br>
- [Discord Voice Agent Commands and Knobs](references/commands.md) <br>
- [Model Routing](references/model-routing.md) <br>
- [Model Settings](references/model-settings.md) <br>
- [One-command Test Mode](references/test-mode.md) <br>
- [Discord Voice Agent Troubleshooting](references/troubleshooting.md) <br>
- [Discord Voice Agent Upgrade Roadmap](references/upgrades.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline commands, configuration names, and implementation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Discord and OpenClaw environment variables, smoke tests, status checks, and local voice capture or history paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
