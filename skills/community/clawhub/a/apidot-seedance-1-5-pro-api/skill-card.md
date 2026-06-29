## Description: <br>
Use APIDot for Seedance 1.5 Pro API workflows covering text-to-video, image-to-video, synchronized audio planning, async tasks, polling, webhooks, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Seedance 1.5 Pro APIDot questions to the right docs, plan async video generation integrations, and handle task IDs, polling, webhooks, and credential boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys or private workflow data could be exposed in client code, logs, screenshots, prompts, media URLs, generated video URLs, callback URLs, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in a backend secret store or server environment and avoid logging or echoing private prompts, media URLs, generated URLs, callback URLs, or credentials. <br>
Risk: Model-specific request fields, availability, pricing, or commercial terms may change after the skill release. <br>
Mitigation: Verify the current APIDot docs and model page before preparing request payloads or making product, reliability, pricing, or availability claims. <br>
Risk: Webhook retries or duplicate callbacks could create duplicate visible results in production queues. <br>
Mitigation: Treat webhook handlers as idempotent and persist task_id, selected model, source media references, request status, and final video URLs together. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-seedance-1-5-pro-api) <br>
- [APIDot Documentation](https://apidot.ai/docs) <br>
- [APIDot Seedance 1.5 Pro Model Page](https://apidot.ai/models/seedance-1-5-pro) <br>
- [APIDot Seedance 1.5 Pro Docs](https://apidot.ai/docs/seedance-1-5-pro) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [Local APIDot Seedance 1.5 Pro Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with documentation links and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; may mention APIDOT_API_KEY handling but does not execute API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
