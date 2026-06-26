## Description: <br>
Generates images from text prompts with MiniMax image-01 and related image models, with guidance for API-key setup and request construction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other external users use this skill to ask an agent for MiniMax image-generation guidance, including prompt-to-image request details, supported aspect ratios, and API-key prerequisites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated image requests are sent to an external MiniMax-compatible API. <br>
Mitigation: Avoid sending private or sensitive prompts, and review the provider's terms and data-handling expectations before use. <br>
Risk: The artifact names both DMXAPI_API_KEY and a MiniMax API key, which may cause configuration mistakes. <br>
Mitigation: Use a dedicated API key where possible and confirm the expected environment variable before running generated requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/dmxapi-image) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax-compatible API key; generated image data depends on the external API response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
