## Description: <br>
Use APIDot for Happy Horse API workflows, including Alibaba Happy Horse video generation, text-to-video API, image-to-video API, reference-to-video API, video editing API, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this documentation-only skill to route APIDot Happy Horse integration questions to the right docs, examples, request modes, async task handling, polling, and webhook guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY exposure through browser code, public repositories, logs, screenshots, or chat output. <br>
Mitigation: Keep the key server-side in environment variables or a backend secret manager, and avoid echoing or logging it. <br>
Risk: Stale or incorrect Happy Horse request fields, availability, limits, or commercial terms. <br>
Mitigation: Verify live APIDot docs and model pages before preparing payloads or making product claims. <br>
Risk: Private prompts, media URLs, callback URLs, or generated video URLs may be exposed during integration work. <br>
Mitigation: Avoid logging sensitive request data and store final video URLs only after a terminal success state. <br>
Risk: Async task handling can produce lost jobs, duplicate visible results, or unsafe retries. <br>
Mitigation: Persist task_id and request state, validate source media URLs, make webhook handlers idempotent, and retry only transient failures with backoff. <br>


## Reference(s): <br>
- [Local APIDot Happy Horse Reference](references/api.md) <br>
- [APIDot Documentation](https://apidot.ai/docs) <br>
- [APIDot Happy Horse Model Page](https://apidot.ai/models/happy-horse) <br>
- [APIDot Happy Horse Docs](https://apidot.ai/docs/happy-horse) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Happy Horse Examples](https://github.com/APIDotAI/happy-horse-api) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no live API calls unless the user explicitly asks and provides a safe server-side environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
