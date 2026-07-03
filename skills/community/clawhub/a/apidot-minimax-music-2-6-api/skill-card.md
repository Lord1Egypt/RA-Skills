## Description: <br>
Use APIDot for MiniMax Music 2.6 API workflows, including AI music generation, lyrics, instrumentals, audio export planning, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to plan APIDot MiniMax Music 2.6 integrations for song, instrumental, lyric, async polling, webhook, and final audio delivery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, private prompts, generated URLs, or callback URLs could be exposed during implementation. <br>
Mitigation: Keep APIDOT_API_KEY server-side, avoid logging sensitive prompts or generated URLs, and store secrets in a backend environment or secret manager. <br>
Risk: APIDot request fields, availability, limits, pricing, or commercial terms may change after this documentation-only release. <br>
Mitigation: Verify live APIDot docs before implementing request payloads or making pricing-sensitive decisions. <br>
Risk: Async task handling can lose or duplicate results if task IDs, polling state, or webhook callbacks are not handled carefully. <br>
Mitigation: Persist task_id and request metadata together, use terminal task status before storing final audio URLs, and make webhook handlers idempotent. <br>


## Reference(s): <br>
- [APIDot API Docs](https://apidot.ai/docs) <br>
- [APIDot MiniMax Music 2.6 Model Page](https://apidot.ai/models/minimax-music-2-6) <br>
- [APIDot MiniMax Music 2.6 Docs](https://apidot.ai/docs/minimax-music-2-6) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot MiniMax Music 2.6 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Code] <br>
**Output Format:** [Markdown guidance with optional code or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code, bundled API client, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
