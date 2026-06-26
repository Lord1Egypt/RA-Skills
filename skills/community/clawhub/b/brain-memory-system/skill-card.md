## Description: <br>
Unified cognitive memory system for agents that provides episodic memory, semantic facts, procedural memory with optional LLM-driven evolution, attention filtering, consolidation, working memory, and memory health checks through a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwmdeadpool](https://clawhub.ai/user/mwmdeadpool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent a local persistent memory system for storing experiences, recalling facts, managing evolving procedures, filtering incoming information, and checking memory health. It is intended for workflows where local SQLite-backed memory and optional LLM-assisted procedure improvement are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive information in memories, facts, procedure steps, or failure logs. <br>
Mitigation: Install only when persistent agent memory is intended, and avoid storing secrets or sensitive records in the memory database. <br>
Risk: Procedure evolution can send procedure history to an external LLM endpoint. <br>
Mitigation: Use proc evolve --dry-run first, prefer a trusted or local LLM endpoint, and provide BRAIN_LLM_KEY from the environment rather than storing it in brain config. <br>
Risk: Shared multi-agent databases can expose one agent's data to another agent through scoped commands. <br>
Mitigation: Use separate databases or avoid shared multi-agent memory unless cross-agent visibility is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mwmdeadpool/brain-memory-system) <br>
- [Publisher Profile](https://clawhub.ai/user/mwmdeadpool) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [CLI text and JSON reports, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and queries a local SQLite memory database; some commands can call an OpenAI-compatible LLM endpoint when procedure evolution is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
