## Description: <br>
Claude 4.5 API on APIDot for Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, Claude 4 5, claude-4-5, Messages API, chat completions, streaming, tool use, coding agents, production chat, API key safety, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route APIDot Claude 4.5 integration questions to the relevant docs, model pages, and implementation guidance. It supports planning for production chat, coding-agent, support-assistant, long-context, streaming, and tool-use workflows without executing code or making API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY could be exposed if copied into browser code, public logs, repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDot API keys in server-side environment variables or a backend secret manager, and avoid logging secrets or private request content. <br>
Risk: Live APIDot calls could be made unintentionally if an agent treats guidance as permission to execute requests. <br>
Mitigation: Allow live API calls only when the user explicitly asks and provides a safe server-side environment. <br>
Risk: Model availability, request fields, limits, or commercial terms may change outside the packaged notes. <br>
Mitigation: Use the current APIDot docs and model pages as the source of truth before preparing production payloads. <br>


## Reference(s): <br>
- [APIDot docs](https://apidot.ai/docs) <br>
- [APIDot Claude 4.5 model page](https://apidot.ai/models/claude-4-5) <br>
- [APIDot Claude 4.5 docs](https://apidot.ai/docs/claude-4-5) <br>
- [APIDot quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot error guidance](https://apidot.ai/docs/errors) <br>
- [APIDot examples](https://github.com/APIDotAI/apidot-examples) <br>
- [APIDot Claude 4.5 Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with documentation links and optional code or configuration examples when requested by the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no bundled scripts, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
