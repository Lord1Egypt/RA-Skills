## Description: <br>
Use APIDot for Seedance 1.0 Pro API workflows, including ByteDance Seedance 1.0 Pro, text-to-video API, image-to-video API, short video generation, 720p and 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Seedance 1.0 Pro text-to-video and image-to-video integrations, including model routing, async task submission, polling, webhook delivery, and safe credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid displaying or logging it. <br>
Risk: Private prompts, media URLs, generated video URLs, or callback URLs could leak through debugging or operational logs. <br>
Mitigation: Avoid logging private prompts, private media URLs, generated video URLs, callback URLs, and other sensitive request data. <br>
Risk: Outdated or guessed APIDot request fields could cause invalid requests or misleading integration guidance. <br>
Mitigation: Review the live APIDot Seedance 1.0 Pro docs before sending requests and do not copy fields from other video model families unless the docs confirm they apply. <br>
Risk: Webhook retries or duplicate callback deliveries could create duplicate visible results. <br>
Mitigation: Treat webhook handlers as idempotent and persist task_id, selected model, user ID, source media references, request status, and final video URLs together. <br>


## Reference(s): <br>
- [Local APIDot Seedance 1.0 Pro Reference](references/api.md) <br>
- [APIDot Documentation](https://apidot.ai/docs) <br>
- [APIDot Seedance 1.0 Pro Model Page](https://apidot.ai/models/seedance-1-0-pro) <br>
- [APIDot Seedance 1.0 Pro API Docs](https://apidot.ai/docs/seedance-1-0-pro) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with API integration notes and occasional code or configuration snippets when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not execute code, make network requests, or store credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
