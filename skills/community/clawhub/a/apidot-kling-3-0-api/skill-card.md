## Description: <br>
Use APIDot for Kling 3.0 API workflows, including Kling 3.0 Standard, Kling 3.0 Pro, Kling 3.0 4K, text-to-video API, image-to-video API, multi-shot video, Native Audio, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Kling 3.0 integration questions to APIDot documentation, plan async text-to-video or image-to-video workflows, and handle task IDs, polling, and webhooks without bundling executable API clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY may be exposed if a user places it in browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDot API keys in a backend secret store or server-side environment variable and avoid echoing credentials in generated examples. <br>
Risk: Model fields, pricing, availability, and API behavior may change after the skill release. <br>
Mitigation: Review the current APIDot docs and Kling 3.0 model page before relying on request fields, limits, commercial terms, or production behavior. <br>
Risk: Generated integration guidance could lead to unintended live API calls if copied into an unsafe environment. <br>
Mitigation: Make live API calls only after the user explicitly requests them and provides a safe server-side environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-kling-3-0-api) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Kling 3.0 Model Page](https://apidot.ai/models/kling-3-0) <br>
- [APIDot Kling 3.0 Docs](https://apidot.ai/docs/kling-3-0) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Kling 3.0 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional code or configuration snippets when requested by the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it includes no executable files, bundled API clients, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
