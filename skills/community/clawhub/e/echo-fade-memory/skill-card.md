## Description: <br>
Runs a thin long-term memory workflow on top of the echo-fade-memory service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiparker](https://clawhub.ai/user/hiparker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use EchoFadeMemory to recall, store, and forget durable preferences, project decisions, corrections, unresolved work, and image or screenshot context through a configured echo-fade-memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and recalls long-term user, project, text, image, and screenshot context, which can include privacy-sensitive material. <br>
Mitigation: Enable it intentionally, point EFM_BASE_URL only at a trusted service, avoid storing secrets or third-party personal data unless retention is deliberate, and use the forget workflow for obsolete or unwanted memories. <br>
Risk: Embedding backends may be local or external depending on deployment configuration. <br>
Mitigation: Confirm whether the configured embedding provider is Ollama, OpenAI, or Gemini before storing sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hiparker/echo-fade-memory) <br>
- [Examples](artifact/references/examples.md) <br>
- [OpenClaw Integration](artifact/references/openclaw-integration.md) <br>
- [OpenClaw Natural Trigger](artifact/references/openclaw-natural-trigger.md) <br>
- [Hook Setup](artifact/references/hooks-setup.md) <br>
- [Memory Templates](artifact/assets/memory-templates.md) <br>
- [Echo Fade Memory for OpenClaw](artifact/bootstrap/EFM_OPENCLAW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable echo-fade-memory service and an embedding backend configured outside the skill.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
