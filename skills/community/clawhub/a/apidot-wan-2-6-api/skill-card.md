## Description: <br>
Use APIDot for Wan 2.6 API workflows, including Wan 2.6 text-to-video API, image-to-video API, video-to-video API, multi-shot video, 720p and 1080p planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Wan 2.6 text-to-video, image-to-video, video-to-video, polling, and webhook workflows while routing implementation details to current APIDot documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys could be exposed if copied into browser code, public repos, logs, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a backend secret manager, and avoid printing secrets in generated examples or troubleshooting output. <br>
Risk: Model-specific request fields, limits, availability, or commercial terms may change outside the skill artifact. <br>
Mitigation: Check the live APIDot Wan 2.6 docs and model page before preparing copyable requests or making API calls. <br>
Risk: Private prompts, source media URLs, callback URLs, or generated video URLs could be leaked through logs or debugging traces. <br>
Mitigation: Redact private prompts and media-related URLs from logs, screenshots, support transcripts, and chat output. <br>
Risk: Async retries or duplicate webhook deliveries could create duplicate or inconsistent visible results. <br>
Mitigation: Persist task_id with the selected model and media references, retry transient failures with backoff, and make webhook handlers idempotent. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Wan 2.6 Model Page](https://apidot.ai/models/wan-2-6) <br>
- [APIDot Wan 2.6 Docs](https://apidot.ai/docs/wan-2-6) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Wan 2.6 Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiehao71727/skills/apidot-wan-2-6-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; real API use requires server-side APIDOT_API_KEY handling and current APIDot docs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
