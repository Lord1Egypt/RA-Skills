## Description: <br>
Use APIDot for Kling 2.6 API workflows, including text-to-video API, image-to-video API, native audio video generation, prompt-driven clips, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route APIDot Kling 2.6 integration questions to the right documentation and plan async video generation workflows without embedding executable API clients or credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or private media details could be exposed if users place APIDOT_API_KEY, prompts, media URLs, generated video URLs, or callback URLs in client-side code, logs, repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in a server-side secret store, avoid logging private prompts or media URLs, and review webhook or polling implementations for credential exposure before making live API calls. <br>
Risk: APIDot Kling 2.6 request fields, availability, limits, or commercial terms may change outside this documentation-only skill. <br>
Mitigation: Use the live APIDot docs and model page as the source of truth before preparing copyable request payloads or making production decisions. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Kling 2.6 Model Page](https://apidot.ai/models/kling-2-6) <br>
- [APIDot Kling 2.6 Docs](https://apidot.ai/docs/kling-2-6) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Kling 2.6 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with documentation links and integration planning notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; produces no executable files, API clients, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
