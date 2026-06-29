## Description: <br>
Use APIDot for Nano Banana Pro API workflows, including image generation API, image editing API, image-to-image API, reference image generation, prompt-based image creation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to plan Nano Banana Pro image generation and image editing integrations through APIDot, including async task submission, polling, webhook handling, and safe API-key placement. It is documentation-only and routes users to current APIDot docs and examples for model-specific request fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if placed in browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager, and avoid logging keys, private prompts, image URLs, callback URLs, or generated image URLs. <br>
Risk: Model fields, pricing, availability, limits, and commercial terms can change outside the packaged skill notes. <br>
Mitigation: Check the current APIDot docs and model page before preparing payloads or relying on product details. <br>
Risk: Live API calls may send user prompts or image references to an external service. <br>
Mitigation: Make live calls only when the user explicitly requests them and provides a safe server-side environment, and validate source image URLs before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiehao71727/apidot-nano-banana-pro-api) <br>
- [APIDot API docs](https://apidot.ai/docs) <br>
- [APIDot Nano Banana Pro model page](https://apidot.ai/models/nano-banana-pro) <br>
- [APIDot Nano Banana Pro docs](https://apidot.ai/docs/nano-banana-pro) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Nano Banana Pro examples](https://github.com/APIDotAI/nano-banana-pro-api) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Nano Banana Pro Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with optional code snippets and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no bundled executable files, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
