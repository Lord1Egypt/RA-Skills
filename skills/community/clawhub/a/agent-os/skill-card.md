## Description: <br>
Persistent agent operating system for OpenClaw. Agents remember across sessions, learn from experience, coordinate on complex projects without duplicate work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocana](https://clawhub.ai/user/cryptocana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use Agent OS to coordinate multi-agent projects with persistent memory, task decomposition, agent routing, execution tracking, and restartable project state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved-state file paths are not safely contained when agent or project IDs are untrusted. <br>
Mitigation: Use only simple trusted agent and project IDs, prefer a fixed storage directory, and validate IDs before production use. <br>
Risk: Project history, goals, outputs, lessons, and errors may be retained in local state. <br>
Mitigation: Avoid secrets or regulated data in persisted fields, and exclude or delete the data directory before sharing or publishing the package. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cryptocana/agent-os) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Build Summary](artifact/BUILD_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON state descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime use can produce local JSON memory and project state files under data/.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
