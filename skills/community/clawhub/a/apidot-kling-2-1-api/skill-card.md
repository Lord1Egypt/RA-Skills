## Description: <br>
Routes agents to APIDot Kling 2.1 documentation and integration guidance for image-to-video workflows, async task submission, polling, webhooks, and API key handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to plan APIDot Kling 2.1 integrations, choose the right documentation path, and handle asynchronous video generation workflows with task IDs, polling, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may guide users toward live APIDot API workflows that consume credits or process user media. <br>
Mitigation: Require explicit user approval before live API calls and use current APIDot documentation for request fields, availability, limits, and commercial terms. <br>
Risk: APIDOT_API_KEY, private prompts, callback URLs, media URLs, or generated video URLs could be exposed through logs or client-side code. <br>
Mitigation: Keep API keys server-side, avoid logging sensitive prompts or URLs, and store task IDs and result URLs only in the intended backend workflow. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Kling 2.1 Model Page](https://apidot.ai/models/kling-2-1) <br>
- [APIDot Kling 2.1 Docs](https://apidot.ai/docs/kling-2-1) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Kling 2.1 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with documentation links and integration planning notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no bundled scripts, automatic network calls, or credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
