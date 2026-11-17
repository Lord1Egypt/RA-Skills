## Description:

Generates images from text prompts with Cloudflare Workers AI free-tier FLUX models, with optional prompt enhancement through Ollama or the calling LLM agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to create image files from text prompts through Cloudflare Workers AI. It can pass through detailed prompts, accept an LLM-enhanced prompt, or use Ollama for optional prompt expansion before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to Cloudflare Workers AI and may also be sent to a configured Ollama server when enhancement is enabled.

Mitigation: Avoid placing secrets, personal data, or confidential information in prompts, and enable Ollama only with local or trusted endpoints.

Risk: Cloudflare credentials are required for generation.

Mitigation: Use a narrowly scoped Cloudflare token, store it in the documented ACCESS credentials file, and keep the file permissions restricted.

Risk: Remote Ollama enhancement can expose prompts to an untrusted network service.

Mitigation: Prefer local Ollama or trusted HTTPS endpoints, and verify network access controls before using a remote host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paradoxfuzzle/skills/cf-img-gen)
- [Cloudflare](https://cloudflare.com)
- [Cloudflare dashboard](https://dash.cloudflare.com)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [files, text, code, shell commands, configuration, guidance]

**Output Format:** [JPEG image file plus MEDIA filepath text; Markdown documentation with JavaScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated images under ~/.openclaw/media/cf-img-gen/ and returns prompt, model, size, and enhancement metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
