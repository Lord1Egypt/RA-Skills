## Description:

Vector-based semantic search for OpenClaw memories. Indexes memory files and enables meaning-based search instead of keyword matching. Uses ChromaDB for local vector storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to index local markdown memory files, search them by meaning or fallback text matching, add memory entries, and inspect memory statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists long-term memory content and creates searchable local copies that may contain sensitive information.

Mitigation: Restrict permissions on ~/.openclaw/semantic-memory/ and ~/.openclaw/workspace/memory/, and review stored content before use on shared systems.

Risk: The documentation asks users to create a Gemini credential file that the security evidence identifies as unused for this version.

Mitigation: Do not create ~/.openclaw/credentials/gemini.json for this version unless a reviewed update requires it.

Risk: The skill depends on ChromaDB, which may change behavior across releases if installed without version controls.

Mitigation: Pin and install chromadb in a controlled environment before deployment.

## Reference(s):

- [Bud Semantic Memory ClawHub listing](https://clawhub.ai/stigg86/skills/bud-semantic-memory)
- [Semantic Memory project homepage](https://github.com/stigg86/semantic-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands; runtime commands print plain-text search results, additions, and stats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw memory markdown files and may persist indexed memory data under the user's home directory.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
