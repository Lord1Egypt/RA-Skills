## Description: <br>
Use APIDot for FLUX.2 API workflows, including image generation, image editing, multi-reference editing, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this documentation skill to route APIDot FLUX.2 image generation and editing questions to the right docs, model pages, async workflow notes, polling guidance, and webhook guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets or a backend secret manager and avoid displaying or logging it. <br>
Risk: Private prompts, private image URLs, generated image URLs, or callback URLs could be logged while building APIDot workflows. <br>
Mitigation: Avoid logging private prompts, image URLs, generated URLs, callback URLs, and other sensitive request details. <br>
Risk: FLUX.2 request fields, limits, availability, or commercial terms may change outside the artifact. <br>
Mitigation: Verify current request fields and product details in APIDot's live docs before making API calls. <br>
Risk: Webhook retries or duplicate callback delivery could create duplicate visible results. <br>
Mitigation: Treat webhook handlers as idempotent and persist task_id, selected model, user ID, source media references, request status, and final image URLs together. <br>


## Reference(s): <br>
- [APIDot FLUX.2 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot FLUX.2 Model Page](https://apidot.ai/models/flux-2) <br>
- [APIDot FLUX.2 Docs](https://apidot.ai/docs/flux-2) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with links and non-executable integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no bundled clients, stored credentials, live API calls, or executable automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
