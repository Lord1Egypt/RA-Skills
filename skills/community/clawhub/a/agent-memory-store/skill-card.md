## Description: <br>
Shared semantic memory store for AI agents. Store, search, and retrieve memories across agents with TTL decay. SQLite persistence - survives restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgnvsk](https://clawhub.ai/user/kgnvsk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run a local memory service for storing, searching, retrieving, and deleting shared memories with optional TTL-based expiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memories are exposed through an unauthenticated HTTP service. <br>
Mitigation: Run only in a controlled environment and bind or firewall port 8768 so only intended local agents can reach it. <br>
Risk: Memory and query text can be sent to OpenAI for embeddings when OPENAI_API_KEY is set. <br>
Mitigation: Unset OPENAI_API_KEY unless external embeddings are intended, and do not store secrets or sensitive personal data. <br>
Risk: Retained SQLite memories may outlive their usefulness. <br>
Mitigation: Periodically inspect and delete the SQLite database or individual memories that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kgnvsk/agent-memory-store) <br>
- [Project homepage](https://kgnvsk.github.io/paylock) <br>
- [OpenAI embeddings API](https://api.openai.com/v1/embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON HTTP responses from the memory service] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local HTTP service on port 8768 and stores memories in a SQLite database.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
