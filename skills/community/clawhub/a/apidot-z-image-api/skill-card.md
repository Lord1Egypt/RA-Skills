## Description: <br>
Use APIDot for Z-Image API workflows, including Alibaba Z-Image, text-to-image API, prompt-based image generation, photorealistic image candidates, aspect ratio planning, safety checker planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to route APIDot Z-Image questions to the correct docs, model pages, and async workflow guidance. It supports planning prompt-based image generation integrations, task submission, polling, webhook delivery, safety checks, and API key handling without making live API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, private prompts, callback URLs, or generated image URLs could be exposed if a future integration logs or surfaces APIDot workflow data. <br>
Mitigation: Keep APIDOT_API_KEY in a backend secret store and avoid exposing private prompts, webhook callback URLs, or generated image URLs in logs, public code, or chat output. <br>
Risk: Model-specific fields, availability, limits, or commercial terms may become stale if copied from memory or another image model family. <br>
Mitigation: Use the live APIDot Z-Image docs and model page as the source of truth before preparing request fields or making product claims. <br>


## Reference(s): <br>
- [APIDot Z-Image Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Z-Image Model Page](https://apidot.ai/models/z-image) <br>
- [APIDot Z-Image Docs](https://apidot.ai/docs/z-image) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with links to APIDot documentation and async workflow notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code, scripts, network operations, or credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
