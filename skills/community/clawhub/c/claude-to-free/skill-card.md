## Description: <br>
Migrate OpenClaw from Claude subscription OAuth to a free or cheap model provider such as OpenRouter, Gemini, or Ollama. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluebirdback](https://clawhub.ai/user/bluebirdback) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose an OpenClaw Claude OAuth setup, choose an alternate provider, update OpenClaw model configuration, restart the gateway, and verify the configured model/auth state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw's configured provider and model and restart the OpenClaw gateway. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before applying changes and verify the configured auth profile and model after restart. <br>
Risk: API keys may be exposed if pasted directly into shell history or shared command transcripts. <br>
Mitigation: Prefer the interactive auth login flow when available and avoid storing provider keys in reusable shell commands. <br>
Risk: The Ollama setup path includes a remote installer command. <br>
Mitigation: Review the remote installer script before executing it and use platform package guidance when required by local policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bluebirdback/claude-to-free) <br>
- [OpenClaw Without Claude Guides](https://github.com/BlueBirdBack/openclaw-without-claude) <br>
- [Free Model List](https://github.com/BlueBirdBack/openclaw-without-claude/blob/main/guides/model-comparison.md) <br>
- [Model Migration Skill Source](https://github.com/BlueBirdBack/openclaw-without-claude/tree/main/skills/model-migration) <br>
- [OpenRouter Keys](https://openrouter.ai/keys) <br>
- [Google AI Studio](https://aistudio.google.com) <br>
- [Ollama Installer](https://ollama.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend provider-specific CLI commands, API-key setup, gateway restart steps, and verification checks.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
