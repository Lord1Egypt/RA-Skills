## Description: <br>
AI image generation with OpenAI GPT Image 2, Azure OpenAI, Google, OpenRouter, DashScope, Z.AI GLM-Image, MiniMax, Jimeng, Seedream, Replicate, Agnes, and Codex CLI APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to generate images from prompts, reference images, aspect ratios, and saved batch prompt files across supported external image providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images may be sent to external image providers. <br>
Mitigation: Use only provider accounts and endpoints approved for the data being submitted, and avoid sensitive local reference images. <br>
Risk: The optional codex-cli provider uses the logged-in Codex session and runs a local subprocess with broad filesystem authority. <br>
Mitigation: Prefer direct API providers for normal use; choose codex-cli only when the user intentionally wants that path and accepts the local execution risk. <br>
Risk: Wrapper or base-url override environment variables can redirect generation through untrusted targets. <br>
Mitigation: Set provider base URLs and wrapper override variables only for endpoints and binaries the operator fully trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/jimliu) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen) <br>
- [Usage Examples](references/usage-examples.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Codex CLI Provider](references/providers/codex-cli.md) <br>
- [Codex OAuth vs OpenAI API key](references/codex-oauth-vs-openai-api-key.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Image files with optional JSON status and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate one image at a time or multiple image files through batch prompt jobs.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
