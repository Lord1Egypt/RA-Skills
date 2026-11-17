## Description:

Searches, stores, and manages agent memory across a local fact store, vector search, BM25 full-text search, and a knowledge graph for workspace knowledge recall and ingestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[primo-studio](https://clawhub.ai/user/primo-studio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to recall workspace knowledge, extract facts from documents or conversations, detect contradictions, auto-ingest Markdown changes, and build entity graphs for local memory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic workspace indexing can capture sensitive Markdown content.

Mitigation: Limit watch and scan paths to intended directories, review MEMORY_WORKSPACE and configured watch paths, and avoid enabling background ingestion until paths are reviewed.

Risk: Persisted memory and raw chunks may store sensitive information in plaintext local files or configured backends.

Mitigation: Review local cache storage, apply filesystem access controls, and avoid storing secrets or regulated data unless the storage location is approved.

Risk: Optional Convex, OpenAI, or OpenRouter settings can send content to remote services despite the local-first workflow.

Mitigation: Keep cloud provider presets and API keys disabled unless remote processing is intended and approved.

Risk: The installer may fetch or configure dependencies from unpinned channels.

Mitigation: Review setup.sh before execution, avoid running it as root, and install Ollama and QMD through trusted pinned channels where possible.

## Reference(s):

- [Configuration Guide](references/configuration.md)
- [Benchmark Results](references/benchmark-results.json)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON/cache memory artifacts when its commands are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
