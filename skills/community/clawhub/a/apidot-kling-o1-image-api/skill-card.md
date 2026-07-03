## Description: <br>
Use APIDot for Kling O1 Image API workflows, including cost-effective image editing, reference-guided image changes, text-to-image planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to route APIDot Kling O1 Image questions to model pages, API docs, async task guidance, polling guidance, and webhook integration notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in a backend secret store or server-side environment variable and avoid logging API keys or private request data. <br>
Risk: APIDot model fields, limits, pricing, and availability can change. <br>
Mitigation: Review the current APIDot docs and model pages before making real API calls or preparing copyable request payloads. <br>
Risk: Async image workflows can lose task state or duplicate visible results if polling and webhook handling are not designed carefully. <br>
Mitigation: Persist task_id, selected model, user ID, media references, status, and final image URLs together, and treat webhook handlers as idempotent. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Kling O1 Image Model Page](https://apidot.ai/models/kling-o1-image) <br>
- [APIDot Kling O1 Image Docs](https://apidot.ai/docs/kling-o1-image) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [Local API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-kling-o1-image-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with API documentation links and integration planning notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable scripts, bundled clients, stored credentials, or automatic API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
