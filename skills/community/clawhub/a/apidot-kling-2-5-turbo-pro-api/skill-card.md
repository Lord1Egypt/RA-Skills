## Description: <br>
Guides agents through APIDot Kling 2.5 Turbo Pro API integration, including text-to-video and image-to-video planning, async task handling, polling, webhooks, and API key safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to route Kling 2.5 Turbo Pro integration questions to APIDot docs and plan prompt-only, start-frame, or start-and-end-frame video workflows. It helps structure async submission, task_id persistence, polling, webhook delivery, and safe API key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated APIDot integration code could expose APIDOT_API_KEY or private prompts, media URLs, callback URLs, or generated video links if copied into unsafe client-side code or logs. <br>
Mitigation: Keep APIDOT_API_KEY in a server-side secret store, avoid logging private request data or generated URLs, and review generated integration code before running it. <br>
Risk: Model fields, limits, availability, and commercial terms may change outside this documentation-only skill. <br>
Mitigation: Use the live APIDot docs and model page as the source of truth before submitting real requests or making product commitments. <br>


## Reference(s): <br>
- [APIDot docs](https://apidot.ai/docs) <br>
- [Kling 2.5 Turbo Pro model page](https://apidot.ai/models/kling-2-5-turbo-pro) <br>
- [Kling 2.5 Turbo Pro API docs](https://apidot.ai/docs/kling-2-5-turbo-pro) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Kling 2.5 Turbo Pro reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with optional code and configuration suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; may guide agents to consult APIDot documentation or draft integration code, but the artifact includes no executables or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
