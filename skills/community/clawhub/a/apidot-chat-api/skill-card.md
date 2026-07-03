## Description: <br>
Use APIDot for chat API workflows, including OpenAI-compatible chat completions, coding assistants, reasoning models, multimodal assistant routing, streaming planning, server-side API key safety, and APIDot chat model docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation-only skill to route APIDot chat integration questions to relevant docs, model pages, examples, and API-key handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys or private chat data could be exposed if copied into browser code, logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY, prompts, transcripts, outputs, and user identifiers in server-side environment variables, secret managers, or approved secure storage. <br>
Risk: APIDot model availability and model-specific request fields can change over time. <br>
Mitigation: Check current APIDot docs and live model pages before choosing a model route or giving model-specific integration details. <br>
Risk: Live API calls could send user data to APIDot unexpectedly. <br>
Mitigation: Do not make live API calls unless the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot documentation](https://apidot.ai/docs) <br>
- [APIDot chat models](https://apidot.ai/models/chat) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [ClawHub skill page](https://clawhub.ai/jiehao71727/skills/apidot-chat-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Code] <br>
**Output Format:** [Markdown guidance with links and optional code or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no scripts, bundled API clients, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
