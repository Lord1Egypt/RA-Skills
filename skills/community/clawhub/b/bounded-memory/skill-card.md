## Description:

Provides full-text search over OpenClaw session history with optional LLM summarization to help recall past conversations, decisions, and context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canmaxfire](https://clawhub.ai/user/canmaxfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Bounded Memory to index local session histories, search prior conversations, and recover past decisions or context. Optional LLM summarization can synthesize matching excerpts when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a local searchable database from private conversation history.

Mitigation: Use offline search only on trusted machines and delete the generated database when it is no longer needed.

Risk: Using --llm can send conversation excerpts and an API credential to a hard-coded external LLM provider.

Mitigation: Enable --llm only when that data transfer is intended and use a dedicated API key with limited scope.

Risk: Manual installation instructions reference repository ownership that does not match the server-resolved publisher.

Mitigation: Prefer ClawHub installation and verify source provenance before manual clone installation.

## Reference(s):

- [Bounded Memory on ClawHub](https://clawhub.ai/canmaxfire/skills/bounded-memory)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and plain-text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline SQLite search by default; optional LLM summarization sends selected excerpts when --llm is used.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact README changelog agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
