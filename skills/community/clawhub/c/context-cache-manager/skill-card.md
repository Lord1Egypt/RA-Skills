## Description: <br>
Provides fork-safe context cloning, message-history compaction, and session restore helpers for OpenClaw-style multi-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suda6632](https://clawhub.ai/user/suda6632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve parent-agent context across spawned child sessions, compact long conversation histories, and restore local session snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive prompts, messages, and content replacement state can be written to local cache files. <br>
Mitigation: Use only on machines and accounts where local conversation snapshots are acceptable; avoid secrets and sensitive work until cache controls, retention, permissions, and cleanup are documented. <br>
Risk: Cached snapshots are reloaded through pickle deserialization. <br>
Mitigation: Review before installation and replace pickle with a safe serialization format before using with untrusted or sensitive cache contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suda6632/context-cache-manager) <br>
- [Publisher profile](https://clawhub.ai/user/suda6632) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Python module and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists compressed local context snapshots and cache index files under an OpenClaw workspace path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
