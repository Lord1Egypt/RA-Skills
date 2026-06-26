## Description: <br>
AI image generation across OpenAI GPT Image 2, Azure OpenAI, Google, OpenRouter, DashScope, Z.AI GLM-Image, MiniMax, Jimeng, Seedream, and Replicate APIs, supporting text-to-image, reference images, aspect ratios, and batch generation from saved prompt files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Baoyu Imagine to generate images from prompts, reference images, and saved prompt batches across supported external image providers. It is suited for text-to-image, identity-preserving edits, aspect-ratio control, and repeatable batch throughput. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected reference images, and possibly reference URLs are sent to the configured external image provider. <br>
Mitigation: Use only approved providers for the task, avoid sensitive local images or internal/signed URLs as references, and confirm what reference data will be sent before generation. <br>
Risk: Provider API keys and custom base URLs can expose credentials or route image data through unintended endpoints. <br>
Mitigation: Keep API keys in the documented environment files or environment variables, restrict access to those files, and review any custom *_BASE_URL settings before running single or batch jobs. <br>
Risk: Reference-image identity preservation can drift or over-stylize subjects when prompts or references are poorly constrained. <br>
Mitigation: Use a small curated reference set and direct identity-preservation wording; avoid long generic descriptions that can cause the provider to synthesize a similar but different subject. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-imagine) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-imagine) <br>
- [Usage examples](references/usage-examples.md) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>
- [Codex Image2 fallback](references/codex-image2-fallback.md) <br>
- [Codex OAuth vs OpenAI API key](references/codex-oauth-vs-openai-api-key.md) <br>
- [DashScope provider guide](references/providers/dashscope.md) <br>
- [MiniMax provider guide](references/providers/minimax.md) <br>
- [OpenRouter provider guide](references/providers/openrouter.md) <br>
- [Replicate provider guide](references/providers/replicate.md) <br>
- [Z.AI provider guide](references/providers/zai.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Image files saved to disk, optional JSON status, and Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured provider credentials; batch mode can produce multiple image files with per-task success or failure status.] <br>

## Skill Version(s): <br>
1.117.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
