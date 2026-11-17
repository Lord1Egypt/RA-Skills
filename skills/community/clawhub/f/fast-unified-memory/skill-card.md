## Description:

Fast Unified Memory provides a Node.js CLI for local unified memory search and storage, combining file-based OpenClaw memory with semantic vector search using Ollama embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add, list, and search local agent memories across OpenClaw files and a local vector store. It is intended for local memory workflows that use Ollama's nomic-embed-text model for embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented curl-to-shell installer can execute an unreviewed installer script.

Mitigation: Install Ollama through a trusted, inspectable method before running the skill.

Risk: Hard-coded OpenClaw memory path and default user id can read or store data in an unintended local workspace.

Mitigation: Change the memory path and user id to the intended local workspace before use.

Risk: Memory content is stored locally in plaintext and processed by the local Ollama service.

Mitigation: Avoid storing highly sensitive material unless plaintext local storage and local processing are acceptable for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/broedkrummen/skills/fast-unified-memory)
- [Ollama](https://ollama.ai)
- [Artifact documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Node.js execution and a running Ollama service with the nomic-embed-text model.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
