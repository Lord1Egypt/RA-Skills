## Description: <br>
Manage a local key-value cache store using bash and Python for caching API responses, session data, or computed results with TTL support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to store, retrieve, search, import, export, and manage local cache entries with TTL metadata during repeated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cache entries are stored locally in plaintext under ~/.cache-tool. <br>
Mitigation: Avoid storing API keys, tokens, credentials, or sensitive session data in the cache. <br>
Risk: Export operations write cache contents to a user-specified path. <br>
Mitigation: Export only to paths that are intended to be created or overwritten. <br>
Risk: Import operations can replace existing cache entries with matching keys. <br>
Mitigation: Treat import files as trusted input and review them before importing. <br>


## Reference(s): <br>
- [Cache on ClawHub](https://clawhub.ai/xueyetianya/cache) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Raw stdout values for get operations; JSON objects for other cache commands; Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cache data is stored locally under ~/.cache-tool with TTL metadata, tags, import/export support, and configurable defaults.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
