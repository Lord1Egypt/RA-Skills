## Description: <br>
Use APIDot async workflow for AI generation APIs, including task submission, task_id handling, polling API, task status API, callback_url, webhook API, retry guidance, idempotent webhook handling, image generation, video generation, music generation, and 3D generation based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design APIDot async generation integrations that persist task IDs, choose polling or webhook delivery, handle retries, and manage result state for image, video, music, and 3D workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this skill may lead an agent to help build workflows that depend on an APIDot API key. <br>
Mitigation: Keep API keys server-side in environment variables or a backend secret manager, and never place them in browser code, public repos, logs, screenshots, or chat output. <br>
Risk: Webhook and polling workflows may expose prompts, source media URLs, final result URLs, or callback URLs through logs or misrouted records. <br>
Mitigation: Avoid logging sensitive workflow data, verify task ownership before attaching results, reconcile polling and webhook events by task_id, and make webhook handlers idempotent. <br>
Risk: Live API calls from uncontrolled environments can leak credentials or create unintended tasks. <br>
Mitigation: Make live API calls only from a controlled backend environment after the user explicitly asks for them. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Models](https://apidot.ai/models) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with code or configuration examples when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable files, bundled clients, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
