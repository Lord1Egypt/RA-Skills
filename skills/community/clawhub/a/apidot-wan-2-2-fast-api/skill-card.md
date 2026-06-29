## Description: <br>
Wan 2.2 Fast API on APIDot for Alibaba Wan 2.2 Fast, wan2.2 text-to-video fast, wan2.2 image-to-video fast, prompt-to-video drafts, one or two image animation, low-cost motion iteration, 480p 720p planning, task_id handling, polling, webhooks, API key safety, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-only skill to route Wan 2.2 Fast video-generation integration questions to APIDot docs, model pages, async task patterns, polling guidance, webhook guidance, and API key safety practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, prompts, media URLs, callback URLs, and generated video URLs can be exposed if copied into frontend code, logs, screenshots, public repositories, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY in server-side environment variables or a secret manager, avoid logging sensitive request data, and only make live API calls from a safe server-side environment. <br>
Risk: Model-specific request fields, availability, limits, and commercial terms may change. <br>
Mitigation: Use the live APIDot docs and model pages as the source of truth before producing copyable request shapes or deployment guidance. <br>
Risk: The security guidance flags admin, email, migration, and external-review commands as sensitive in environments where those workflows are present. <br>
Mitigation: Install only where those workflows are intended, and confirm targets, dry-run output, recipients, and production deployment names before allowing writes or sends. <br>


## Reference(s): <br>
- [APIDot Wan 2.2 Fast Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [Wan 2.2 Fast Model Page](https://apidot.ai/models/wan-2-2-fast) <br>
- [Wan 2.2 Fast Docs](https://apidot.ai/docs/wan-2-2-fast) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [ClawHub Release Page](https://clawhub.ai/jiehao71727/skills/apidot-wan-2-2-fast-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with links and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no scripts, clients, stored credentials, or automatic network calls are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
