## Description: <br>
Local-first memory retrieval for Agent/OpenClaw workspaces that need explainable answers from MEMORY.md and memory/*.md instead of a remote memory platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to retrieve and explain prior decisions, incidents, preferences, policy notes, and change history from local Markdown memory files. It is best suited for local or self-hosted agent workspaces that need transparent memory retrieval without a hosted memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may contain secrets, personal data, incident details, or business-sensitive notes. <br>
Mitigation: Review MEMORY.md and memory/*.md before installation or use, and protect or delete .memory-index when the indexed copy is no longer needed. <br>
Risk: Local memory snippets can be sent to SiliconFlow automatically when rerank is enabled and an API key is present. <br>
Mitigation: Set MEMORY_RERANK=0 for hard local-only operation when memory contents should not leave the workspace. <br>
Risk: A generic API_KEY environment variable may unintentionally enable external reranking. <br>
Mitigation: Avoid exposing a generic API_KEY in the environment used to run this skill; use explicit, scoped credentials only when reranking is intended. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Regression Cases](references/regression-cases.json) <br>
- [Regression Queries](references/regression-queries.md) <br>
- [Publish Plan](references/publish-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ranked memory matches, snippets, scores, source file names, and explanation fields; can build local index files under .memory-index/.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
