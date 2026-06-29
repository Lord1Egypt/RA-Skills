## Description: <br>
Use APIDot for Wan 2.5 API workflows, including Alibaba Wan 2.5, text-to-video API, image-to-video API, optional audio text planning, short video generation, 480p 720p 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to plan APIDot Wan 2.5 text-to-video and image-to-video integrations, including model routing, async task handling, polling, webhooks, and secure API-key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, prompts, source media URLs, callback URLs, and generated video URLs may be sensitive. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets, avoid logging sensitive request data or generated URLs, and make live APIDot calls only from an intended server-side environment. <br>
Risk: Model request fields, availability, limits, and commercial terms may change outside the artifact. <br>
Mitigation: Use the current APIDot docs and model pages before preparing payloads or making product claims. <br>
Risk: Webhook retries or duplicate deliveries may create duplicate visible results if handlers are not idempotent. <br>
Mitigation: Persist task IDs and statuses together and treat webhook handlers as idempotent. <br>


## Reference(s): <br>
- [APIDot Wan 2.5 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Wan 2.5 Model Page](https://apidot.ai/models/wan-2-5) <br>
- [APIDot Wan 2.5 Docs](https://apidot.ai/docs/wan-2-5) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API integration notes and code-planning recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable files, hidden automation, network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
