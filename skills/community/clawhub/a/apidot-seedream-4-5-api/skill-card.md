## Description: <br>
Use APIDot for Seedream 4.5 API workflows, including image generation API, image editing API, image-to-image API, reference image generation, prompt-based image creation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan APIDot Seedream 4.5 image generation and editing integrations, including request routing, async task handling, polling, webhooks, and credential-safe implementation practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY could be exposed through browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep the key server-side in environment variables or a backend secret manager and avoid logging it. <br>
Risk: Private prompts, image URLs, generated image URLs, or callback URLs could disclose user or workflow data if logged. <br>
Mitigation: Avoid logging private prompts, private image URLs, generated image URLs, callback URLs, and related request metadata. <br>
Risk: Outdated or guessed APIDot request fields could lead to failed or incorrect Seedream 4.5 integrations. <br>
Mitigation: Verify the live APIDot docs and model page before preparing payloads or making API calls. <br>
Risk: Live API calls could run in an unsafe environment or before the user is ready. <br>
Mitigation: Do not make live APIDot API calls unless the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot documentation](https://apidot.ai/docs) <br>
- [APIDot Seedream 4.5 model page](https://apidot.ai/models/seedream-4-5) <br>
- [APIDot Seedream 4.5 docs](https://apidot.ai/docs/seedream-4-5) <br>
- [APIDot webhooks documentation](https://apidot.ai/docs/webhooks) <br>
- [APIDot Seedream 4.5 examples](https://github.com/APIDotAI/seedream-4.5-api) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Seedream 4.5 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with optional code snippets and API workflow notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not make API calls, bundle clients, or store credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
