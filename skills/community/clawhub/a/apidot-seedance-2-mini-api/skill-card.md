## Description: <br>
Use APIDot for Seedance 2.0 Mini API workflows, including low-cost short video generation, text-to-video, first and last frame image-to-video, reference image/video/audio workflows, 480p, 720p, task_id, polling, webhooks, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this documentation-only skill to route Seedance 2.0 Mini integration questions to APIDot model pages, docs, request-planning notes, polling guidance, and webhook guidance. It supports planning text-to-video, first/last-frame, and reference-guided short video workflows without making API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys, private prompts, media URLs, callback URLs, generated video URLs, and task IDs may be exposed if included in client code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY server-side, store secrets in a backend secret manager or environment variable, and avoid logging sensitive prompts, media URLs, callback URLs, generated URLs, or task IDs. <br>
Risk: Model-specific request fields, availability, limits, and commercial terms can change outside this documentation-only skill. <br>
Mitigation: Use the live APIDot docs and Seedance 2.0 Mini model page as the source of truth before preparing payloads or making product commitments. <br>
Risk: Live API calls from an unsafe environment can leak credentials or sensitive media data. <br>
Mitigation: Make live APIDot requests only when explicitly requested by the user and only from a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot Seedance 2.0 Mini Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Seedance 2.0 Mini Model Page](https://apidot.ai/models/seedance-2-mini) <br>
- [APIDot Seedance 2.0 Mini Docs](https://apidot.ai/docs/seedance-2-mini) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with documentation links and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable scripts, bundled API client, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
