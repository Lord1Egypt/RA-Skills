## Description: <br>
Use APIDot for Gemini 3 API workflows, including Gemini 3 Flash Preview, Gemini 3 Pro Preview, native generateContent, streamGenerateContent, Gemini chat, coding assistants, streaming, tool planning, API key safety guidance, and APIDot docs routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan APIDot Gemini 3 integrations, choose documentation paths, and handle Gemini chat, streaming, generateContent, coding assistant, support assistant, and tool-planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDot API keys or private prompts could be exposed if copied into browser code, public logs, public repositories, screenshots, or chat output. <br>
Mitigation: Keep APIDOT_API_KEY and private request context in server-side environment variables or a backend secret manager, and avoid logging secrets, private prompts, customer data, tool arguments, or generated responses that may contain sensitive data. <br>
Risk: Model-specific request fields, availability, limits, commercial terms, or streaming behavior may change. <br>
Mitigation: Use the current APIDot Gemini 3 docs and model page as the source of truth before preparing payloads or making implementation decisions. <br>
Risk: Live APIDot calls may send user data or incur external-service effects. <br>
Mitigation: Make live API calls only when the user explicitly asks and provides a safe server-side environment. <br>


## Reference(s): <br>
- [APIDot Gemini 3 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Gemini 3 Docs](https://apidot.ai/docs/gemini-3) <br>
- [APIDot Gemini 3 Model Page](https://apidot.ai/models/gemini-3) <br>
- [APIDot Quickstart](https://apidot.ai/docs/quickstart) <br>
- [APIDot Error Guidance](https://apidot.ai/docs/errors) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with links and optional inline configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no bundled scripts, API clients, stored credentials, or automatic network calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
