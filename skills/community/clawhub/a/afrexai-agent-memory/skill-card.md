## Description: <br>
Complete zero-dependency memory system for AI agents — file-based architecture, daily notes, long-term curation, context management, heartbeat integration, and memory hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to set up durable file-based memory for AI agents, including active context, curated long-term memory, daily notes, topic files, and archives. It is intended for agents that need persistent recall without external APIs, databases, or cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may retain private records, secrets, or regulated personal data if users store them there. <br>
Mitigation: Treat MEMORY.md and the memory/ directory as private records, avoid storing secrets or regulated personal data, and review retained notes regularly. <br>
Risk: The documented memory_search and memory_get workflows may rely on platform-specific tools rather than purely manual file search. <br>
Mitigation: Confirm the target agent environment supports the referenced search and retrieval workflow, or substitute equivalent local file search before depending on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-agent-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with file templates and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory architecture instructions and maintenance practices; no external services are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
