## Description:

Provides LM Studio or Ollama users with a browser-based local LLM chat interface for offline or low-connectivity use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinflw](https://clawhub.ai/user/robinflw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who already run local models use this skill to start a browser chat UI, configure local or OpenAI-compatible LLM endpoints, customize persona prompts, and run diagnostics for offline use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model output can trigger reads of arbitrary local file paths and place file contents into the chat context.

Mitigation: Use the file-read feature only when the requested path is expected and acceptable; do not expose sensitive files through the chat.

Risk: Prompts, persona text, chat content, and automatically read file snippets can be sent to the configured LLM endpoint.

Mitigation: Use only trusted local LLM endpoints, keep the service bound to 127.0.0.1, and avoid remote or untrusted --llm-url values.

Risk: The skill's privacy posture depends on local configuration despite offline-focused documentation.

Mitigation: Review endpoint and host settings before use and run diagnostics to confirm the intended local setup.

## Reference(s):

- [AirplaneAI GitHub repository](https://github.com/robinflw/Airplane-AI)
- [AirplaneAI GitHub references](https://github.com/robinflw/Airplane-AI/tree/main/references)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local endpoint selection, persona file use, browser launch, diagnostics, and offline chat operation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
