## Description: <br>
Use APIDot for Hailuo 2.3 API workflows, including MiniMax Hailuo 2.3, text-to-video API, image-to-video API, start image guidance, prompt optimization, duration and resolution planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan APIDot Hailuo 2.3 text-to-video and image-to-video integrations, route work to the current APIDot documentation, and handle asynchronous task submission, polling, and webhook patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated integration guidance could become stale as APIDot request fields, pricing, limits, or webhook behavior change. <br>
Mitigation: Review APIDot's live documentation before implementing or running a Hailuo 2.3 workflow. <br>
Risk: Real API integrations require an APIDOT_API_KEY that could be exposed if placed in client-side code, logs, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets only and avoid logging API keys, private prompts, media URLs, generated video URLs, or callback URLs. <br>


## Reference(s): <br>
- [APIDot Hailuo 2.3 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Hailuo 2.3 Model Page](https://apidot.ai/models/hailuo-2-3) <br>
- [APIDot Hailuo 2.3 Docs](https://apidot.ai/docs/hailuo-2-3) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with documentation links and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code, bundled clients, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
