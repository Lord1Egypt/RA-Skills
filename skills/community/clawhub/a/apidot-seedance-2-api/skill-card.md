## Description: <br>
Use APIDot for Seedance 2 API workflows, including Seedance 2 Fast, text-to-video, image-to-video, native-audio video generation, reference media workflows, async task submission, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to plan and implement APIDot Seedance 2 video-generation workflows, including request-mode selection, async task submission, polling, and webhook integration. It can also help prepare safe server-side use of the optional submit script when the user explicitly asks for a live request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live APIDot submissions can expose API keys, private prompts, media URLs, callback URLs, or generated video URLs if run from an unsafe environment or logged. <br>
Mitigation: Keep APIDOT_API_KEY in a server-side secret store, review payloads before using the submit script, and avoid submitting private data unless sharing it with APIDot is acceptable. <br>
Risk: Outdated or guessed Seedance 2 request details can produce invalid jobs or misleading integration guidance. <br>
Mitigation: Use the current APIDot docs and model pages for model-specific fields, availability, limits, and commercial terms before preparing or submitting payloads. <br>


## Reference(s): <br>
- [APIDot docs](https://apidot.ai/docs) <br>
- [APIDot Seedance 2 model page](https://apidot.ai/models/seedance-2) <br>
- [APIDot Seedance 2 docs](https://apidot.ai/docs/seedance-2) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot webhooks](https://apidot.ai/docs/webhooks) <br>
- [APIDot Seedance 2 reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference APIDOT_API_KEY and curl; optional live submissions require an explicit user request and a reviewed payload.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
