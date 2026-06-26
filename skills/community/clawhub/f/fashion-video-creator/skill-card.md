## Description: <br>
Generates virtual model image requests, Seedance 2.0 video prompts, and operator SOPs for single or batch fashion e-commerce videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and e-commerce teams use this skill to generate fashion product video prompts, virtual model image requests, and Jimeng operator steps for outfit showcase content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Volcano Engine API key and may send fashion prompts, product imagery, or model details to external generation services. <br>
Mitigation: Use a dedicated revocable key, avoid sensitive assets, and review prompts before generation. <br>
Risk: External generation services can incur paid API usage. <br>
Mitigation: Monitor API usage and confirm model or endpoint settings before running batch jobs. <br>
Risk: Default audience, tone, or gender assumptions may not fit the intended content. <br>
Mitigation: Override the dialogue style, audience, and model settings when they do not match the campaign requirements. <br>


## Reference(s): <br>
- [Fashion Video Creator on ClawHub](https://clawhub.ai/dingtom336-gif/fashion-video-creator) <br>
- [Model Presets](references/model-presets.md) <br>
- [Seedream API Call Specifications](references/seedream-api.md) <br>
- [Prompt Assembly](references/prompt-assembly.md) <br>
- [Dialogue Library](references/dialogue-library.md) <br>
- [Volcano Engine Ark API](https://ark.cn-beijing.volces.com) <br>
- [Jimeng Platform](https://jimeng.jianying.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown with generated prompts, SOP steps, and optional image generation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single and batch modes; requires ARK_API_KEY and Seedream model or endpoint access.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
