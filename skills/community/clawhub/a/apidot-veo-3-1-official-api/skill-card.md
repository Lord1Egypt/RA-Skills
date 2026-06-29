## Description: <br>
Use APIDot for Veo 3.1 Official API workflows, including model routing, text-to-video, image-to-video, first and last frame control, reference video, native audio planning, async task submission, polling, webhooks, and APIDot documentation routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation-only skill to plan APIDot Veo 3.1 Official integrations, choose the right APIDot documentation path, and handle async video generation workflows with task IDs, polling, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY could be exposed if copied into browser code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep the key server-side in environment variables or a backend secret manager and avoid displaying it in generated guidance. <br>
Risk: An agent may propose live APIDot calls when the user only needs planning or documentation guidance. <br>
Mitigation: Only allow live APIDot calls when the user explicitly asks and provides a safe server-side environment. <br>
Risk: Prompts, private media URLs, callback URLs, and generated video URLs may contain sensitive workflow data. <br>
Mitigation: Avoid logging or echoing these values, and treat webhook handlers as idempotent to prevent duplicate visible results. <br>
Risk: Model fields, availability, limits, and commercial terms may change in APIDot's live service. <br>
Mitigation: Use the current APIDot docs and model pages as the source of truth before preparing payloads or making product claims. <br>


## Reference(s): <br>
- [APIDot documentation](https://apidot.ai/docs) <br>
- [APIDot Veo 3.1 Official model page](https://apidot.ai/models/veo-3-1-official) <br>
- [APIDot Veo 3.1 Official API docs](https://apidot.ai/docs/veo-3-1-official) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-veo-3-1-official-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with links, routing notes, and integration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; may mention APIDOT_API_KEY handling but does not include executable code or stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
