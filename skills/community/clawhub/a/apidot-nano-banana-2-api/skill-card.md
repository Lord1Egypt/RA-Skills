## Description: <br>
Use APIDot for Nano Banana 2 API workflows, including Gemini 3.1 Flash Image API, nano-banana-2, nano-banana-2-edit, text-to-image API, image editing API, readable text image generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Nano Banana 2 image generation and editing questions to APIDot documentation, examples, and async integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot workflows may involve an APIDOT_API_KEY. <br>
Mitigation: Keep the key in server-side environment variables or a backend secret manager, and never expose it in browser code, logs, screenshots, repositories, or chat output. <br>
Risk: Live API calls could use private prompts, source image URLs, generated image URLs, or callback URLs. <br>
Mitigation: Only make live calls when the user intentionally provides a safe server-side environment, and avoid logging private prompts or URLs. <br>
Risk: Nano Banana 2 model fields, limits, availability, and commercial terms may change. <br>
Mitigation: Use current APIDot docs and model pages for request fields and product details instead of guessing or copying fields from other model families. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Nano Banana 2 Model Page](https://apidot.ai/models/nano-banana-2) <br>
- [APIDot Nano Banana 2 Docs](https://apidot.ai/docs/nano-banana-2) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Nano Banana 2 Examples](https://github.com/APIDotAI/nano-banana-2-api) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [Local APIDot Nano Banana 2 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no bundled executable files, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
