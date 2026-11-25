## Description:

Generate images, video and audio with Affogato (affogato.ai) from a coding agent — list models, quote the credit price, create a generation, wait for it and download the outputs — using an Affogato API key or the Affogato MCP server. Use when the user wants an AI image, video, voiceover, lipsync, headshot or product shot made with Affogato, or asks about Affogato models and prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[affogato.ai](https://clawhub.ai/user/affogato.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to find Affogato models, estimate credit costs, generate image, video, or audio media, and retrieve the resulting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is suspicious, citing a credential-routing weakness and incomplete disclosure about permissions and media uploads.

Mitigation: Before use, verify that you trust Affogato with your API key and uploaded media, review the configured service destination and permissions, and account for unresolved path-like references because scan coverage is incomplete.

## Reference(s):

- [Affogato developer documentation](https://affogato.ai/developers)
- [Affogato API OpenAPI specification](https://api.affogato.ai/v1/openapi.json)
- [Affogato MCP setup](https://affogato.ai/mcp)
- [Prompting notes](artifact/references/prompting.md)

## Skill Output:

**Output Type(s):** [Images, Video, Audio, Files, API Calls]

**Output Format:** [Generated image, video, and audio files or output URLs, with JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected model and user inputs; generation uses plan credits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
