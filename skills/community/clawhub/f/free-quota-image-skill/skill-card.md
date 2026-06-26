## Description: <br>
Generate images from text with a free-quota-first multi-provider workflow for Hugging Face, Gitee, ModelScope, A4F, and OpenAI-compatible endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChiayenGu](https://clawhub.ai/user/ChiayenGu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate one or more images from text prompts while routing across free-quota-oriented image providers, rotating tokens on quota or authentication failures, and returning structured generation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and prompt-optimized text may be sent to external providers. <br>
Mitigation: Avoid sensitive, proprietary, or regulated prompt text; disable prompt optimization when privacy requirements call for minimizing provider exposure. <br>
Risk: Provider tokens and OpenAI-compatible endpoint settings are sensitive configuration. <br>
Mitigation: Use trusted tokens and endpoints, keep openai_compatible disabled unless the endpoint is controlled or trusted, and inject secrets through environment configuration rather than committed files. <br>
Risk: The CLI loads .env files from nearby directories, which can expose unrelated environment variables during execution. <br>
Mitigation: Run the skill from a dedicated workspace and avoid placing unrelated sensitive .env files in the working directory or parent skill directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChiayenGu/free-quota-image-skill) <br>
- [Project homepage](https://github.com/Amery2010/peinture) <br>
- [Provider Endpoints](references/provider-endpoints.md) <br>
- [Model Matrix](references/model-matrix.md) <br>
- [Token Rotation Policy](references/token-rotation-policy.md) <br>
- [Prompt Optimization Policy](references/prompt-optimization-policy.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON generation results, direct image URLs, optional downloaded image files, and Markdown guidance with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful JSON output includes generation metadata such as provider, model, prompts, seed, aspect ratio, fallback chain, and elapsed time; batch mode returns an images array.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
