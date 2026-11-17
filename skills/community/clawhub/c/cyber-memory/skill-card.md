## Description:

Five-layer memory system with automatic fact extraction via local LLM (Ollama) that processes session transcripts locally with no external API required by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[witnesssun](https://clawhub.ai/user/witnesssun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add local-first persistent memory, fact extraction, session snapshots, and searchable session continuity to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook reads recent session transcripts and writes memory files automatically.

Mitigation: Install only in workspaces where automatic transcript summarization and local memory writes are acceptable.

Risk: Recent transcript content and an API key can be sent to a configurable OpenAI-compatible endpoint.

Mitigation: Keep baseUrl pointed at localhost for local Ollama processing unless remote processing is intentional and trusted.

Risk: A global OpenAI provider key or OPENAI_API_KEY could be forwarded to an untrusted endpoint if configuration is changed.

Mitigation: Review hook configuration before enabling it and avoid exposing global provider keys in environments that use untrusted endpoints.

## Reference(s):

- [Cyber Memory on ClawHub](https://clawhub.ai/witnesssun/skills/cyber-memory)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON5 configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local Markdown memory files, extracted facts, compaction snapshots, and session reset logs when the hook runs.]

## Skill Version(s):

1.0.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
