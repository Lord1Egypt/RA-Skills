## Description:

Enhanced memory search with hybrid vector+keyword scoring, temporal routing, filepath scoring, adaptive weighting, pseudo-relevance feedback, salience scoring, and knowledge graph cross-references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameseball](https://clawhub.ai/user/jameseball)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to index, search, and maintain workspace memory files with hybrid retrieval, salience scoring, and cross-reference graph support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory and workspace notes can be copied into memory/vectors.json as plaintext chunks.

Mitigation: Treat generated vector and cross-reference files as sensitive data and restrict filesystem permissions before use in shared environments.

Risk: Source text and search queries can be sent to the configured embedding endpoint.

Mitigation: Keep OLLAMA_URL pointed at a trusted local Ollama instance unless the user has approved sending memory content to another endpoint.

Risk: The skill reads memory files and selected workspace-level notes during indexing and salience scoring.

Mitigation: Review the memory directory and core workspace files before indexing, and remove secrets or private notes that should not be searchable.

## Reference(s):

- [Enhanced Memory Skill Page](https://clawhub.ai/jameseball/skills/enhanced-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with command examples, JSON search results, and generated index files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include file paths, line numbers, scores, snippets, headers, salience prompts, and cross-reference graph statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
