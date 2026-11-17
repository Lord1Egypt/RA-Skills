## Description:

Provides one zero-dependency interface for calling Anthropic, OpenAI, Google, xAI, Mistral, and Ollama models while switching models through configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to route a single chat interface across cloud AI providers or local Ollama models without rewriting provider-specific request code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and conversation context may be sent to the selected cloud AI provider when a cloud model is configured.

Mitigation: Install only when that data flow is intended; use Ollama for local-only operation and avoid secrets or regulated data in prompts unless approved.

Risk: Configuring unnecessary provider credentials increases exposure if the runtime environment is compromised.

Mitigation: Configure only the API keys for providers actually used by the skill.

## Reference(s):

- [AI Provider Bridge ClawHub Page](https://clawhub.ai/theshadowrose/skills/ai-provider-bridge)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration]

**Output Format:** [JavaScript module API returning provider response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured API keys for selected cloud providers; Ollama can be used for local-only operation.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
