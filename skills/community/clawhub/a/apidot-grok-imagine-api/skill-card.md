## Description: <br>
Use APIDot for Grok Imagine API workflows, including xAI Grok Imagine image generation, image editing, text-to-video, image-to-video, Grok Imagine Video 1.5, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Grok Imagine image and video integration questions to APIDot documentation, async task workflow guidance, polling, and webhook implementation notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real APIDot integrations require an API key that could be exposed if placed in browser code, public repos, logs, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY server-side in environment variables or a backend secret manager, and avoid echoing secrets in generated examples. <br>
Risk: Prompts, media URLs, callback URLs, and generated result URLs may contain private user or workflow data. <br>
Mitigation: Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated result URLs. <br>
Risk: Async media jobs can be mishandled if task identifiers, status, selected model, user context, or result URLs are not persisted together. <br>
Mitigation: Persist task_id, selected model, user ID, source media references, request status, and final media URLs together before polling or webhook processing. <br>


## Reference(s): <br>
- [APIDot Grok Imagine Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Grok Imagine Model Page](https://apidot.ai/models/grok-imagine) <br>
- [APIDot Grok Imagine Docs](https://apidot.ai/docs/grok-imagine) <br>
- [APIDot Grok Imagine Video 1.5 Docs](https://apidot.ai/docs/grok-imagine-video-1-5) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with links, integration notes, and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable files, bundled clients, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
