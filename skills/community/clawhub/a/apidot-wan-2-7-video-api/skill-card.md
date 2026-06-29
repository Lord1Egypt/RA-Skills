## Description: <br>
Use APIDot for Wan 2.7 Video API workflows, including text-to-video API, image-to-video API, reference-to-video, edit-video, Wan 2.7, async task submission, task_id handling, polling, task status, webhook integration, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route Wan 2.7 Video integration work to APIDot documentation, async task guidance, webhook planning, and model-specific reference notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys or private media details could be exposed if copied into frontend code, logs, screenshots, or chat output. <br>
Mitigation: Store APIDOT_API_KEY only in server-side environment variables or a backend secret manager, and avoid logging private prompts, media URLs, generated video URLs, callback URLs, or credentials. <br>
Risk: Live APIDot requests may create cost, privacy, or workflow side effects if made unintentionally. <br>
Mitigation: Make live API calls only after explicit user intent and from a safe server-side environment. <br>
Risk: Model-specific fields, limits, availability, or commercial terms may be outdated if inferred from local notes. <br>
Mitigation: Use the current APIDot docs and model page as the source of truth before preparing request payloads or making claims. <br>


## Reference(s): <br>
- [APIDot Wan 2.7 Video Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Wan 2.7 Video Model Page](https://apidot.ai/models/wan-2-7-video) <br>
- [APIDot Wan 2.7 Video Docs](https://apidot.ai/docs/wan-2-7-video) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; live API calls require explicit user intent and a server-side APIDOT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
