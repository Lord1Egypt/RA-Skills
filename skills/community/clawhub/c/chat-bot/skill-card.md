## Description: <br>
LLM chat interface using OpenAI-compatible APIs with streaming support and session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when working with the pywayne.llm.chat_bot module to create OpenAI-compatible chat clients, manage streaming responses, configure model parameters, and maintain independent chat sessions with history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if copied into shared code or chat transcripts. <br>
Mitigation: Store provider credentials in a secret manager or environment variables and avoid committing real keys in examples or configuration. <br>
Risk: Chat prompts and session history may contain sensitive user or business data. <br>
Mitigation: Treat prompts, system messages, and history as sensitive data; avoid sending confidential content to unapproved providers. <br>
Risk: Misconfigured base URLs can send requests to untrusted or unintended model endpoints. <br>
Mitigation: Use only approved OpenAI-compatible endpoints and verify the pywayne package source before using the skill with real data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/chat-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python code examples and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers OpenAI-compatible endpoints, streaming and non-streaming calls, session history, and chat configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
