## Description: <br>
Grok Imagine Video 1.5 API on APIDot for xAI image-to-video generation, reference image animation, prompt-guided motion, short video clips, duration planning, 480p 720p planning, async task submission, task_id handling, polling, webhooks, API key safety, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Grok Imagine Video 1.5 integrations, route to the right APIDot docs, and handle async image-to-video workflows with polling or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys and request data can expose credentials, prompts, private media URLs, callback URLs, or generated video links. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets, avoid logging sensitive request or result data, and do not place keys or private URLs in browser code, public repositories, screenshots, or chat output. <br>
Risk: Live APIDot calls may submit media-generation jobs or trigger webhook workflows unintentionally. <br>
Mitigation: Only make live API calls when the user explicitly asks and provides a controlled server-side environment; use polling for local testing and idempotent webhook handlers for production workflows. <br>
Risk: Model-specific request fields, availability, limits, and commercial terms may change over time. <br>
Mitigation: Use the current APIDot docs and model page as the source of truth before generating copyable request examples or implementation details. <br>


## Reference(s): <br>
- [APIDot Grok Imagine Video 1.5 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [Grok Imagine Video 1.5 Model Page](https://apidot.ai/models/grok-imagine-video-1-5) <br>
- [Grok Imagine Video 1.5 API Docs](https://apidot.ai/docs/grok-imagine-video-1-5) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it includes no executable scripts and makes no automatic network requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
