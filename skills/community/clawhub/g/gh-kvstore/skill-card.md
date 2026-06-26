## Description: <br>
In-memory key-value store with TTL for AI agents. Set, get, delete, list, flush, and stats. Supports any JSON value, optional TTL per key, and prefix-based key listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a lightweight local key-value API for agent state, caching, and data sharing with optional per-key TTL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local API includes unauthenticated delete and flush endpoints that can remove stored values. <br>
Mitigation: Keep the service bound to localhost, control access to the port, and use the flush endpoint only when clearing all in-memory keys is intended. <br>
Risk: Stored values are held in memory by a temporary local service and may include sensitive data if users choose to store it. <br>
Mitigation: Avoid storing secrets unless the runtime and port access are controlled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/gh-kvstore) <br>
- [Publisher Profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON HTTP responses from a local FastAPI service, with Markdown examples for shell usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [In-memory storage only; values may expire by TTL, and flush deletes all current keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
