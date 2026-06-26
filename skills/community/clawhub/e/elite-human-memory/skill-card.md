## Description: <br>
Elite Human Memory provides a portable ClawHub-compatible memory system for LLM agents with working, episodic, semantic, and optional vector memory layers plus metadata, promotion, conflict handling, and retrieval guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cliftonwknox](https://clawhub.ai/user/cliftonwknox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add structured, searchable cross-session memory to ClawHub, custom, or multi-agent deployments while keeping storage paths and vector search implementation configurable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cross-session memory can retain sensitive conversation history, secrets, or regulated personal data. <br>
Mitigation: Require explicit user approval before writing memories, avoid storing secrets or regulated personal data, and provide clear inspection and deletion controls. <br>
Risk: Vector storage or external persistent stores can expose memory content outside the local environment if enabled without review. <br>
Mitigation: Keep vector storage local unless deliberately enabled, and review any external vector database configuration before deployment. <br>
Risk: Stale or conflicting memories can lead the agent to retrieve misleading context. <br>
Mitigation: Use confidence, state, source, and expiration metadata, log conflicts, and ask the user to resolve higher-severity contradictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cliftonwknox/elite-human-memory) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Integration examples](artifact/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with pseudocode examples and file layout conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Framework-agnostic; optional vector index; no external service dependency unless the host configures one] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact README.md and SKILL.md list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
