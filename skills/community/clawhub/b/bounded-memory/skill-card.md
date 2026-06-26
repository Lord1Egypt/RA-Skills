## Description: <br>
Searches OpenClaw session histories locally with SQLite FTS5 so an agent can recall prior conversations, decisions, preferences, and context; optional LLM summarization is disabled by default and only runs with --llm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canmaxfire](https://clawhub.ai/user/canmaxfire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to index and search their OpenClaw conversation history when they need to recall prior discussions, decisions, or project context. It is most useful for local session search, with optional LLM summarization only when enabled by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated sessions.db can contain private prompts, client data, decisions, or secrets from indexed OpenClaw sessions. <br>
Mitigation: Treat sessions.db as sensitive local data, restrict file access, and delete it when it is no longer needed. <br>
Risk: Using --llm can send matched session snippets to MiniMax and can use API keys from OpenClaw config or environment variables. <br>
Mitigation: Keep --llm disabled unless external summarization is acceptable, and verify which API key and provider will be used before enabling it. <br>


## Reference(s): <br>
- [Bounded Memory on ClawHub](https://clawhub.ai/canmaxfire/bounded-memory) <br>
- [Hermes Agent bounded memory inspiration](https://github.com/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text guidance with shell commands and search result excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search is offline by default; --llm can send matched snippets to the MiniMax API for summarization.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
