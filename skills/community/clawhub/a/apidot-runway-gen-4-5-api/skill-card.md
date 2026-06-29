## Description: <br>
Use APIDot for Runway Gen-4.5 API workflows, including text-to-video, image-to-video, cinematic motion planning, async task submission, polling, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route APIDot Runway Gen-4.5 questions to current documentation, plan text-to-video or image-guided video workflows, and reason about async task polling or webhook delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, prompts, media URLs, generated video URLs, or callback URLs could be exposed during real APIDot integrations. <br>
Mitigation: Keep APIDOT_API_KEY server-side, avoid logging private prompts or media URLs, and review generated integration guidance before use. <br>
Risk: APIDot request fields, limits, model availability, or commercial terms may change after this documentation-only skill was released. <br>
Mitigation: Verify current model-specific request fields and product details in the official APIDot docs before implementation. <br>
Risk: Async video jobs can be mishandled if task IDs, polling states, or webhook callbacks are not persisted and processed carefully. <br>
Mitigation: Persist task_id and status metadata, use webhook handlers idempotently, and retry only transient failures with backoff. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Runway Gen-4.5 Model Page](https://apidot.ai/models/runway-gen-4-5) <br>
- [APIDot Runway Gen-4.5 Docs](https://apidot.ai/docs/runway-gen-4-5) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [Local APIDot Runway Gen-4.5 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration guidance] <br>
**Output Format:** [Markdown guidance with links, workflow notes, and integration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code, bundled API client, stored credentials, or automatic API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
