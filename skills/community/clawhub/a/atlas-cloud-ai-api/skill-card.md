## Description: <br>
Helps agents generate images and videos, call OpenAI-compatible LLM chat APIs, and draft Atlas Cloud integration code using one Atlas Cloud API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihhhh](https://clawhub.ai/user/xixihhhh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Atlas Cloud image generation, video generation, and LLM chat into applications, including model selection, CLI/script usage, and API request examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, uploaded files, and chat messages are sent to Atlas Cloud for processing, and generated outputs may be hosted on its CDN. <br>
Mitigation: Avoid confidential or regulated data unless policy permits, review Atlas Cloud data handling terms before use, and treat generated output URLs as externally hosted content. <br>
Risk: API usage may incur cost or fail because of invalid keys, insufficient balance, rate limits, or provider errors. <br>
Mitigation: Use revocable API keys, monitor billing, handle 401/402/429/5xx responses, and apply retries with backoff where appropriate. <br>
Risk: The image script can also use a Gemini API key when the Google provider is explicitly selected. <br>
Mitigation: Confirm which provider is selected before execution and keep provider-specific credentials scoped and revocable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihhhh/atlas-cloud-ai-api) <br>
- [Image generation reference](references/image-gen.md) <br>
- [Video generation reference](references/video-gen.md) <br>
- [LLM chat reference](references/llm-chat.md) <br>
- [Model reference and selection guide](references/models.md) <br>
- [Atlas Cloud model list API](https://console.atlascloud.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples, model-selection guidance, and commands that require ATLASCLOUD_API_KEY.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
