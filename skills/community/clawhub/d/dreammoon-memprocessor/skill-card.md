## Description: <br>
Enables AI agents to maintain persistent multi-layer memories and generate experience-driven personas through a local FastAPI memory service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local memory persistence, semantic search, and persona generation or evolution workflows to AI agents. It is intended for agent systems that need remembered context across sessions and API-accessible persona state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service may retain personal or sensitive agent memory over long periods. <br>
Mitigation: Avoid storing secrets or regulated data, review what agents send to the service, and set retention practices before enabling persistent storage. <br>
Risk: The local API can expose stored memory and persona state if bound broadly or left unprotected. <br>
Mitigation: Bind the service to localhost or place it behind authentication and network access controls before use. <br>
Risk: The seeded MEMORY.md template includes relationship and loyalty content that may be inappropriate for other deployments. <br>
Mitigation: Remove or replace the seeded template content before first run and audit generated memory files after setup. <br>
Risk: The delete API is advertised but evidence indicates deletion is not implemented across all storage layers. <br>
Mitigation: Do not rely on API deletion for data erasure; manually inspect and remove data from Redis, SQLite, Markdown memory files, and vector archives when needed. <br>


## Reference(s): <br>
- [DreamMoon MemProcessor ClawHub Release](https://clawhub.ai/zfanmy/dreammoon-memprocessor) <br>
- [zfanmy ClawHub Publisher Profile](https://clawhub.ai/user/zfanmy) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Privacy and Project Notice](artifact/VERSION-ISOLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local service instructions and API-oriented agent integration guidance; runtime behavior may create persistent memory files, SQLite data, Redis entries, and vector indexes.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
