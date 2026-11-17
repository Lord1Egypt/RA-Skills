## Description:

Provides guidance for using the pywayne.llm.chat_bot module to create OpenAI-compatible LLM chat clients with streaming, conversation history, and session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when implementing synchronous LLM chat flows against OpenAI-compatible APIs, including streaming responses, multi-turn history, custom model settings, and independent chat sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat prompts and responses may be sent to an external OpenAI-compatible provider.

Mitigation: Use only trusted and approved provider endpoints, and avoid sending secrets or sensitive data unless the provider is approved for that data.

Risk: Conversation history may retain sensitive context across turns or sessions.

Mitigation: Clear history when it is no longer needed and configure a finite session timeout when retained chat history is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/chat-bot)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes example base URLs, API key configuration, model parameters, streaming usage, and session timeout settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
