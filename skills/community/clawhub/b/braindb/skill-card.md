## Description: <br>
Persistent, semantic memory for AI agents. Gives your AI long-term recall that survives compaction and session resets - 98% accuracy, 20ms latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chair4ce](https://clawhub.ai/user/Chair4ce) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use BrainDB to add persistent semantic memory to OpenClaw agents, including automatic capture, storage, and recall of relevant conversation and workspace context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory queries, conversation turns, or migrated workspace content may be sent to Gemini when Gemini processing or swarm migration is intentionally configured. <br>
Mitigation: Use local-only migration, avoid configuring GEMINI_KEY unless external Gemini processing is intended, and review data flows before enabling optional Gemini-backed features. <br>
Risk: The skill creates durable long-term memories from agent conversations, workspace files, tool outcomes, and environment details. <br>
Mitigation: Review or skip execution-awareness.js when tool and environment details should not be stored, and scan migrations before importing workspace content. <br>
Risk: The local gateway can be open to other local processes if API authentication is not enabled. <br>
Mitigation: Set BRAINDB_API_KEY when other local processes are a concern and keep the gateway bound to localhost. <br>


## Reference(s): <br>
- [BrainDB ClawHub Page](https://clawhub.ai/Chair4ce/braindb) <br>
- [Publisher Profile](https://clawhub.ai/user/Chair4ce) <br>
- [BrainDB Release Download](https://github.com/Chair4ce/braindb/releases/download/v0.5.0/braindb-v0.5.0.zip) <br>
- [BrainDB Documentation](https://github.com/Chair4ce/braindb#readme) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, shell commands, guidance] <br>
**Output Format:** [JSON API responses, recalled memory text, Markdown setup guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and recalls episodic, semantic, procedural, and association memories through a local gateway.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release metadata; artifact frontmatter and package.json show 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
