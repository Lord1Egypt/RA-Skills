## Description:

Generate and edit images through Filtrix Remote MCP. Use when users ask to create images or refine existing ones. Supports gpt-image-1, nano-banana, and nano-banana-2 through one MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate new images and refine existing images through Filtrix Remote MCP using supported gpt-image-1, nano-banana, and nano-banana-2 modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An endpoint override can send the Filtrix API key and user image data to an arbitrary URL.

Mitigation: Use the default Filtrix MCP endpoint or only set FILTRIX_MCP_URL to a trusted HTTPS endpoint.

Risk: Remote image generation or editing may process private screenshots, IDs, proprietary images, or regulated data through Filtrix.

Mitigation: Avoid sending sensitive images or regulated data unless remote Filtrix processing is approved for that use.

Risk: Returned downloads are not size- or type-checked before being saved.

Mitigation: Save outputs only to intended paths and inspect generated files before reuse or distribution.

Risk: Generation and editing requests may consume account credits.

Mitigation: Use a dedicated API key with limited privileges or credits and use idempotency keys for retry protection.

## Reference(s):

- [MCP Tools Reference](references/mcp-tools.md)
- [gpt-image-1 Mode](references/gpt-image-1.md)
- [nano-banana Mode](references/nano-banana.md)
- [nano-banana-2 Mode](references/nano-banana-2.md)
- [Prompt Guide](references/prompts.md)
- [Filtrix AI Prompt Library](https://www.filtrix.ai/prompts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated image file paths or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Filtrix MCP API key; generation and editing requests may consume account credits.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
