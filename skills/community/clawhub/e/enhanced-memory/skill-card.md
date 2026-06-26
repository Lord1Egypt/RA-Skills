## Description: <br>
Enhanced memory search with hybrid vector+keyword scoring, temporal routing, filepath scoring, adaptive weighting, pseudo-relevance feedback, salience scoring, and knowledge graph cross-references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesEBall](https://clawhub.ai/user/JamesEBall) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to index, search, cross-reference, and prioritize markdown memory files in an OpenClaw workspace using local scripts and an Ollama embedding endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory files and named core markdown files, which may contain sensitive or stale information. <br>
Mitigation: Use it only on workspaces where that content is appropriate to index, and review the generated memory index files periodically. <br>
Risk: Indexed content and search queries are sent to the configured Ollama embedding endpoint. <br>
Mitigation: Keep OLLAMA_URL pointed at a trusted local endpoint unless remote processing is intentional and approved. <br>
Risk: The skill stores searchable vector, cross-reference, query, and access data locally under the memory directory. <br>
Mitigation: Delete or regenerate those local JSON files when memory content changes or when retained index data is no longer appropriate. <br>


## Reference(s): <br>
- [Enhanced Memory on ClawHub](https://clawhub.ai/JamesEBall/enhanced-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus script outputs as text or JSON depending on the invoked utility.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include scored memory snippets; indexing and graph utilities write local JSON files under the memory directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
