## Description: <br>
AI image generation via Cloudflare Workers AI with FLUX models and optional prompt enhancement through Ollama or the calling LLM agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to generate image files from text prompts through Cloudflare Workers AI. It can optionally expand short prompts with the calling LLM agent or an Ollama host before generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Cloudflare Workers AI and, when Ollama enhancement is enabled, to the configured Ollama host. <br>
Mitigation: Avoid secrets or confidential text in prompts and use localhost or a trusted private Ollama server. <br>
Risk: The skill requires Cloudflare credentials stored in an ACCESS credential file. <br>
Mitigation: Use a least-privilege Cloudflare token and restrict the credential file permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paradoxfuzzle/cf-img-gen) <br>
- [Cloudflare](https://cloudflare.com) <br>
- [Cloudflare dashboard](https://dash.cloudflare.com) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JPEG image file, MEDIA file path, and JSON result object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated images under ~/.openclaw/media/cf-img-gen and returns prompt, model, size, and enhancement metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
