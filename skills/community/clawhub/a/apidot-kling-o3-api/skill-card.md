## Description: <br>
Use APIDot for Kling O3 API workflows, including Kling O3 Standard, Kling O3 Pro, Kling O3 4K, text-to-video API, image-to-video API, reference video generation, multi-shot video, Native Audio, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to plan APIDot Kling O3 video workflows, route questions to current APIDot docs, and handle asynchronous task, polling, and webhook integration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using APIDot API keys or private media in live integrations can expose secrets or sensitive content if handled client-side or logged. <br>
Mitigation: Keep APIDOT_API_KEY server-side, avoid logging prompts, media URLs, callback URLs, and generated video URLs, and use backend secret management for live API calls. <br>
Risk: Model fields, pricing, availability, and workflow details may change after this documentation-only release. <br>
Mitigation: Check the current APIDot docs and model pages before relying on request fields, commercial terms, or model availability. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Kling O3 model page](https://apidot.ai/models/kling-o3) <br>
- [APIDot Kling O3 docs](https://apidot.ai/docs/kling-o3) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Kling O3 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with documentation links and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable code, API client, credential storage, or automatic network calls are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
