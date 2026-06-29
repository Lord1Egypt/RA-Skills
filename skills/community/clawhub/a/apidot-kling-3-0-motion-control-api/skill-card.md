## Description: <br>
Kling 3.0 Motion Control API on APIDot for kling 3 0 motion control, kling-3-0-motion-control, motion transfer, reference video to character image, dance transfer, action transfer, controllable animation, image-to-video, task_id, polling, webhooks, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route APIDot Kling 3.0 Motion Control integration work to the right model pages, docs, async task pattern, polling guidance, and webhook guidance. It supports motion-transfer video workflows that use a character image and reference motion video for controllable animation, dance transfer, action transfer, storyboard previews, or ad creative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, frontend bundles, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager and avoid logging credentials or private media URLs. <br>
Risk: Model-specific payload fields, availability, limits, or commercial terms may change over time. <br>
Mitigation: Use the live APIDot docs and model page as the source of truth before preparing request payloads or making claims. <br>
Risk: Async video jobs can produce duplicate or stale workflow state if task IDs and webhook callbacks are not handled carefully. <br>
Mitigation: Persist task_id and related media references together, poll or process callbacks only until terminal status, and make webhook handlers idempotent. <br>


## Reference(s): <br>
- [Local APIDot Kling 3.0 Motion Control reference](references/api.md) <br>
- [APIDot docs](https://apidot.ai/docs) <br>
- [APIDot Kling 3.0 Motion Control model page](https://apidot.ai/models/kling-3-0-motion-control) <br>
- [APIDot Kling 3.0 Motion Control docs](https://apidot.ai/docs/kling-3-0-motion-control) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with documentation links, integration notes, and configuration reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no bundled executable files, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
