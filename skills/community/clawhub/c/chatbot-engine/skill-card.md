## Description:

Chatbot Engine supports multi-turn dialogue, intent recognition, context management, and knowledge-base retrieval for chatbot applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add chatbot behavior, intent classification, multi-turn dialogue state, knowledge-base retrieval, and optional LLM-backed responses to agent applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and conversation context may be sent to OpenAI or Anthropic when those providers are enabled.

Mitigation: Enable external LLM providers only after privacy review and user disclosure, and keep mock or local providers for development where appropriate.

Risk: Unreviewed dependency versions can introduce supply-chain or compatibility risk.

Mitigation: Install in an isolated environment and pin, scan, and review dependencies before production use.

Risk: Custom regex intent definitions or plugin objects can change chatbot behavior in unsafe or unexpected ways.

Mitigation: Limit intent configuration and plugin registration to trusted administrators and review behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/chatbot-engine)
- [Project homepage](https://github.com/openclaw/chatbot-engine)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Python code with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce chatbot text responses, intent labels, extracted entities, retrieved knowledge-base answers, and optional LLM-provider responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
