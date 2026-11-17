## Description:

ai-capabilities routes persona management, emotion analysis, photo generation, text-to-speech, and image generation requests through standardized MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route AI capability requests to configured MCP services for persona profiles, emotion analysis, identity-aware photo generation, TTS, and image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route requests to configured MCP services and use SILICONFLOW_API_KEY for generation.

Mitigation: Install it only with intended MCP services configured, keep the API key scoped and revocable, and review requested tool actions before execution.

Risk: Persona-changing requests can update local persona state such as SOUL.md and influence future agent behavior.

Mitigation: Review persona updates before running them and keep auditable backups or version control for persona state files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-capabilities)
- [CosyVoice reference data](artifact/scripts/cosyvoice_reference.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Guidance]

**Output Format:** [Structured JSON tool responses, text guidance, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured ai-capabilities and TTS MCP services plus SILICONFLOW_API_KEY for supported generation paths.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
