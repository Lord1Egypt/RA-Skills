## Description: <br>
Zero-vector AI memory engine with self-learning, local SQLite storage, REST memory APIs, and optional user-configured LLM reranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenroudeyu-collab](https://clawhub.ai/user/wenroudeyu-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local conversational memory, memory search, fact extraction, and recall context to OpenClaw-style agents through a local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and processes personal conversational memory locally, which can include sensitive information. <br>
Mitigation: Run it in an isolated environment first, avoid storing sensitive memories, and regularly inspect or delete data in the cc-soul and OpenClaw data directories. <br>
Risk: The local API can expose memory data if bound beyond localhost or allowed through a firewall. <br>
Mitigation: Keep the API bound to localhost or restrict access with host firewall rules before using it with real data. <br>
Risk: Optional LLM and CLI features may send memory-derived context to user-configured external services. <br>
Mitigation: Leave remote LLM and CLI features disabled unless needed, and use only reviewed endpoints and credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenroudeyu-collab/cc-soul) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory API responses and configuration guidance; optional LLM behavior depends on user-supplied credentials.] <br>

## Skill Version(s): <br>
3.2.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
