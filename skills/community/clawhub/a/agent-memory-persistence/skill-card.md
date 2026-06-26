## Description: <br>
Provide long-term memory persistence for AI agents with SQLite-backed storage, structured metadata, vector embeddings, semantic retrieval, lifecycle management, and queries by user, session, and time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add durable local memory to AI agents, including structured metadata storage, session and user filtering, expiration cleanup, and semantic retrieval over embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories may persist sensitive user or session data across agent runs. <br>
Mitigation: Avoid storing secrets, credentials, payment data, or unnecessary personal information, and define a retention policy before enabling persistent memory. <br>
Risk: The SQLite database may be readable by other local users or processes if stored in an unprotected path. <br>
Mitigation: Use a protected database path and apply restrictive file permissions or encryption where required. <br>
Risk: Expired or obsolete memories may remain available if cleanup is not called. <br>
Mitigation: Use expiresAt, delete, and cleanupExpired as part of regular memory lifecycle management. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imgolye/agent-memory-persistence) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [TypeScript library APIs and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local SQLite-backed memory records with optional metadata, embeddings, expiration timestamps, and query results.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
