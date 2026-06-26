## Description: <br>
Dual-Brain runs a background daemon that generates short second-opinion perspectives from a secondary LLM provider for OpenClaw agent messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dannydvm](https://clawhub.ai/user/Dannydvm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agent developers use this skill to give OpenClaw agents a secondary model perspective before responding. It is intended for workflows where a short alternative view can help surface missing angles, validation points, or reasoning risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent conversation content and local memory context may be sent to the selected secondary LLM provider. <br>
Mitigation: Use a local provider such as Ollama for sensitive work and avoid enabling external providers for confidential sessions. <br>
Risk: The daemon stores configuration and generated perspectives locally, including API keys when non-local providers are configured. <br>
Mitigation: Restrict permissions on ~/.dual-brain/config.json and review local perspective files before sharing the machine or workspace. <br>
Risk: The skill can install a persistent background service through launchd or systemd. <br>
Mitigation: Review the generated service configuration before enabling background persistence and stop or uninstall the service when it is no longer needed. <br>
Risk: Automatically generated secondary perspectives may be incomplete, stale, or misleading. <br>
Mitigation: Treat perspectives as advisory input and have the primary agent synthesize and verify them before using them in a response. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Dannydvm/dual-brain) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown perspective files and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Perspectives are written as latest-per-agent Markdown files under the configured local perspectives directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
