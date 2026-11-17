## Description:

Generate and edit images through Cloudflare Workers AI using text-to-image and image-to-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slippersheepig](https://clawhub.ai/user/slippersheepig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate new images or transform source images through Cloudflare Workers AI, then return the resulting image files through the active chat provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudflare API tokens can be exposed if credential verification prints environment variable values.

Mitigation: Use a presence-only credential check, and keep CF_API_TOKEN out of logs, shell history, and source control.

Risk: Prompts and selected source images are sent to Cloudflare Workers AI for inference.

Mitigation: Use the skill only with data appropriate for Cloudflare Workers AI and the user's organizational data-handling rules.

Risk: An overbroad Cloudflare API token increases impact if the token is exposed.

Mitigation: Use a least-privilege Cloudflare token limited to the Workers AI inference permission needed for the target account.

## Reference(s):

- [Cloudflare Workers AI Images on ClawHub](https://clawhub.ai/slippersheepig/skills/cloudflare-workers-ai-images)
- [Docker Compose environment example](references/docker-compose-env-example.md)
- [Cloudflare Workers AI API endpoint](https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and local PNG file paths printed to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated or edited images are saved as local PNG files for chat handoff; normal use relies on temporary file storage unless the user asks to keep a copy.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
