## Description: <br>
Use APIDot for Seedream 5.0 Lite API workflows, including image generation, image editing, multi-reference generation, reference-guided editing, structured layout planning, async task submission, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Seedream 5.0 Lite integration questions to APIDot model pages, API docs, async task patterns, polling guidance, and webhook guidance. It supports planning image generation and editing workflows without bundling executable code or stored credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY or private media data could be exposed during real integration work. <br>
Mitigation: Keep API keys server-side, avoid logging private prompts or image URLs, and use a backend secret manager or environment variables for real API calls. <br>
Risk: Model request fields, pricing, availability, or commercial terms may change after the skill release. <br>
Mitigation: Verify current fields and terms in the live APIDot docs and model page before submitting production requests. <br>


## Reference(s): <br>
- [Local APIDot Seedream 5.0 Lite Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Seedream 5.0 Lite Model Page](https://apidot.ai/models/seedream-5-0-lite) <br>
- [APIDot Seedream 5.0 Lite Docs](https://apidot.ai/docs/seedream-5-0-lite) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with documentation links and concise integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable files, automatic network calls, or credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
