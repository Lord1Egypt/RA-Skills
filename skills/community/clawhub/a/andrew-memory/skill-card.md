## Description: <br>
Product-grade semantic memory layer for AI agents using LanceDB, with long-term memory, semantic search, Core Identity management, and conversation distillation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panyuugit](https://clawhub.ai/user/panyuugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent semantic memory, identity retrieval, and conversation distillation to OpenClaw agents. It is intended for agents that need to remember user facts, retrieve past context, or maintain continuity across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists user facts and conversation-derived memories in a local LanceDB directory. <br>
Mitigation: Install only when long-term agent memory is desired, avoid storing secrets or confidential data, and review or remove ~/.andrew-memory/data when memories must be cleared. <br>
Risk: In API mode, memory or conversation text may be sent to MiniMax for embeddings or distillation. <br>
Mitigation: Use local Ollama mode for private work or when conversation text should not leave the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panyuugit/andrew-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration] <br>
**Output Format:** [OpenClaw tool response text with JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local LanceDB memory records and may call MiniMax or local Ollama services depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
