## Description:

a2e.ai Full Platform provides API and CLI guidance for generating and managing images, videos, face and head swaps, speech, voice clones, avatars, talking media, dubbing, caption removal, virtual try-on, photobooks, storage, and task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to call the a2e.ai media platform for image generation, video generation, face and head swap, voice cloning, avatars, dubbing, caption removal, virtual try-on, storage, status polling, and account balance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an A2E API key and its documentation sources a shared workspace credential file.

Mitigation: Provide only A2E_KEY through a scoped secret or clean environment, and install only when you trust a2e.ai with media generation and account management access.

Risk: Face, voice, avatar, dubbing, and virtual try-on features can process identity-sensitive media.

Mitigation: Use only media you own or are authorized to use, and require explicit confirmation before cloning identities or uploading media.

Risk: The CLI can spend credits and delete remote account assets.

Mitigation: Require explicit confirmation before spending credits or deleting remote assets, and review generated commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielgrobelny/skills/a2e-image)
- [a2e.ai Platform](https://video.a2e.ai)
- [a2e.ai API Index](https://api.a2e.ai/llms.txt)
- [a2e.ai API Token Guide](https://api.a2e.ai/getting-api-tokens-2025-version-1063013m0.md)
- [a2e.ai Pricing](https://video.a2e.ai/live_pricing)
- [Complete API Reference](references/api-complete.md)
- [API Key Reference](references/api-key.md)
- [Full API Overview](references/api-overview.md)
- [OpenAPI Endpoints](references/openapi-endpoints.json)
- [Pricing Reference](references/pricing.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires A2E_KEY and may create, upload, poll, list, or delete remote a2e.ai media assets.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
