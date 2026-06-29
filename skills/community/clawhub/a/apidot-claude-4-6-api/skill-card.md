## Description: <br>
Use APIDot for Claude 4.6 API workflows, including Claude Sonnet 4.6, Claude Opus 4.6, Messages API, chat completions, streaming, tool use planning, production chat, coding agents, API key safety guidance, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to find APIDot Claude 4.6 documentation paths and plan API integrations for chat, coding-agent, streaming, tool-use, and long-context workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY or private prompt data could be exposed through frontend code, logs, screenshots, repositories, or chat output. <br>
Mitigation: Keep API keys server-side in environment variables or a secret manager, and avoid logging keys, private prompts, customer data, tool arguments, private context, or sensitive generated output. <br>
Risk: Claude 4.6 request fields, limits, availability, or commercial terms may change outside the bundled reference notes. <br>
Mitigation: Use current APIDot docs and model pages as the source of truth before preparing payloads or making product claims. <br>
Risk: A live APIDot API call could be made when the user only wanted documentation or planning guidance. <br>
Mitigation: Make live API calls only when the user explicitly asks and a safe server-side environment is available. <br>


## Reference(s): <br>
- [APIDot Claude 4.6 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Claude 4.6 Docs](https://apidot.ai/docs/claude-4-6) <br>
- [APIDot Claude 4.6 Model Page](https://apidot.ai/models/claude-4-6) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Error Guidance](https://apidot.ai/docs/errors) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with optional code and configuration snippets when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable files, automatic network calls, or stored credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
