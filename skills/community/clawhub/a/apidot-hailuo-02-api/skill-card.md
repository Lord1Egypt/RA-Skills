## Description: <br>
Use APIDot for Hailuo 02 API workflows, including MiniMax Hailuo 02, Hailuo 02 Pro, text-to-video API, image-to-video API, first frame and last frame guidance, physics-aware short video, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Hailuo 02 integration questions to APIDot documentation, model pages, and async workflow guidance for text-to-video, image-to-video, polling, and webhook patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys, private prompts, media URLs, callback URLs, or generated video URLs could be exposed if copied into unsafe environments or logs. <br>
Mitigation: Keep APIDOT_API_KEY in server-side secrets and avoid logging private prompts, media URLs, callback URLs, API keys, or generated video URLs. <br>
Risk: Live APIDot API calls may be made unintentionally or from an unsafe client-side environment. <br>
Mitigation: Make live API calls only when the user explicitly requests them and provides a safe backend environment. <br>


## Reference(s): <br>
- [APIDot Hailuo 02 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Hailuo 02 Model Page](https://apidot.ai/models/hailuo-02) <br>
- [APIDot Hailuo 02 Docs](https://apidot.ai/docs/hailuo-02) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with documentation links and implementation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable files, bundled API client, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
