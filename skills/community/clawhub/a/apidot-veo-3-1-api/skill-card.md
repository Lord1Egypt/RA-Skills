## Description: <br>
Use APIDot for Veo 3.1 API workflows, including Google Veo API, veo3.1-lite, veo3.1-fast, veo3.1-quality, text-to-video API, image-to-video API, reference image video, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Veo 3.1 integrations, choose APIDot documentation paths, handle async task submission and status workflows, and optionally submit a reviewed payload from a trusted server-side shell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY is required for live API calls and could expose account access if copied into client code, logs, payload files, screenshots, or chat output. <br>
Mitigation: Keep the key in a trusted server-side environment or secret manager and do not include it in payloads, frontend bundles, public repositories, logs, screenshots, or conversation output. <br>
Risk: The optional submit script can send a live Veo 3.1 request to APIDot when explicitly invoked. <br>
Mitigation: Run the script only from a trusted server-side shell after reviewing the JSON payload and confirming the user requested a live submission. <br>
Risk: Prompts, source media URLs, callback URLs, task IDs, and generated video URLs can contain sensitive workflow or customer data. <br>
Mitigation: Treat those values as sensitive, persist task IDs and result URLs privately, and avoid logging or sharing them unless the user explicitly permits it. <br>


## Reference(s): <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Veo 3.1 Model Page](https://apidot.ai/models/veo-3-1) <br>
- [APIDot Veo 3.1 Docs](https://apidot.ai/docs/veo-3-1) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Veo 3.1 Examples](https://github.com/APIDotAI/veo-3.1-api) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Veo 3.1 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command usage and JSON payload handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference APIDOT_API_KEY and curl requirements; live API submission is user-invoked only.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
