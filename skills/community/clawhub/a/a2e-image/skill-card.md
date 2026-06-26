## Description: <br>
a2e.ai full API: Image Gen (Text2Image, NanoBanana, GPT Image, Flux 2), Video Gen (Image2Video with LoRA/FLF2V support, Video2Video, Kling 3.0, Wan 2.6, Sora 2, Veo 3.1, Seedance), Face/Head Swap, TTS + Voice Clone, AI Avatars, Talking Photo/Video, AI Dubbing, Caption Removal, Virtual Try-On, Photobook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgrobelny](https://clawhub.ai/user/danielgrobelny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a2e.ai media-generation APIs for images, videos, face and head swaps, voice cloning, avatars, dubbing, caption removal, virtual try-on, and related account tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, media URLs, uploaded assets, and generated content to a third-party media-generation service. <br>
Mitigation: Use only data approved for a2e.ai processing, avoid private or internal URLs, and review the service terms before sending sensitive images, audio, video, or prompts. <br>
Risk: Face swap, voice clone, avatar, and dubbing features can create sensitive or identity-based media. <br>
Mitigation: Run these features only with clear rights and consent for the people, voices, likenesses, and source media involved. <br>
Risk: The helper can spend account credits and includes delete or remove commands for user assets. <br>
Mitigation: Check pricing and balance before paid operations, and manually verify task, avatar, voice, face, and media IDs before deletion commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielgrobelny/a2e-image) <br>
- [a2e.ai platform](https://video.a2e.ai) <br>
- [a2e.ai API index](https://api.a2e.ai/llms.txt) <br>
- [a2e.ai pricing](https://video.a2e.ai/live_pricing) <br>
- [Complete API Reference](references/api-complete.md) <br>
- [API Key Guide](references/api-key.md) <br>
- [Full API Overview](references/api-overview.md) <br>
- [OpenAPI Endpoints](references/openapi-endpoints.json) <br>
- [Pricing Reference](references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, API request details, and JSON responses from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires A2E_KEY and may initiate paid asynchronous media-generation or account-management tasks against a2e.ai.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
