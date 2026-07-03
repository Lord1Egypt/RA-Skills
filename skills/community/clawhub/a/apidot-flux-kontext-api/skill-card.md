## Description: <br>
Use APIDot for Flux Kontext API workflows, including Flux Kontext Pro, Flux Kontext Max, text-to-image API, context-aware image editing, character consistency, local edits, typography-aware visual updates, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Flux Kontext image generation and editing work through APIDot documentation, model pages, and async integration guidance. It helps plan prompt-only generation, image editing, polling, webhook handling, and API key handling without bundling executable clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY could be exposed if copied into browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep the key in server-side environment variables or a backend secret manager, and avoid logging API keys, private prompts, image URLs, generated image URLs, or callback URLs. <br>
Risk: Flux Kontext request fields, limits, availability, or terms may change after the skill release. <br>
Mitigation: Review the live APIDot docs and model pages before implementing production workflows or preparing copyable request examples. <br>
Risk: Webhook retries or duplicate callbacks can create duplicate visible results. <br>
Mitigation: Treat webhook handlers as idempotent and persist task_id, selected model, user ID, request status, source media references, and final image URLs together. <br>


## Reference(s): <br>
- [APIDot Flux Kontext Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Flux Kontext Model Page](https://apidot.ai/models/flux-kontext) <br>
- [APIDot Flux Kontext Docs](https://apidot.ai/docs/flux-kontext) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with links and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable files, bundled API clients, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
