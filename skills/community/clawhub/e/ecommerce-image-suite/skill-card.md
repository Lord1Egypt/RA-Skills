## Description: <br>
ecommerce-image-suite helps agents turn product images and selling points into marketplace-ready ecommerce image suites, including prompts, generated product images, and optional text overlays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzj177](https://clawhub.ai/user/wzj177) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, catalog operators, and ecommerce content teams use this skill to create product image suites for domestic and international marketplaces from a product image plus structured selling-point information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product descriptions, prompts, and provider credentials can be sent to selected image providers or custom proxy URLs. <br>
Mitigation: Use official provider endpoints when possible, configure custom *_BASE_URL values only for endpoints you control and trust, and avoid sending sensitive product information unless the provider is approved for that data. <br>
Risk: Provider checks can expose partial API key prefixes in command output. <br>
Mitigation: Do not share provider-check output publicly, and rotate any credential whose prefix or surrounding context has been disclosed. <br>
Risk: Long-lived or broad provider API keys increase impact if a configured endpoint or local environment is compromised. <br>
Mitigation: Use least-privilege provider keys, store them in environment variables or approved local configuration, and rotate them regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzj177/ecommerce-image-suite) <br>
- [Platform specifications](references/platforms.md) <br>
- [Image type specifications](references/image-types.md) <br>
- [Analysis prompts](references/analysis-prompts.md) <br>
- [Provider API configuration](references/providers.md) <br>
- [OpenAI image generation endpoint](https://api.openai.com/v1/images/generations) <br>
- [Google image generation endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent) <br>
- [Stability AI image generation endpoint](https://api.stability.ai/v2beta/stable-image/generate/core) <br>
- [DashScope image generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>
- [Volcengine Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON inputs, shell command examples, generated image files, and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image suites may include raw product images, final overlaid JPEGs, and per-step JSON status files.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
