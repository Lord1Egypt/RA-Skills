## Description:

Structured episodic, semantic, and procedural memory framework for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durtydhiana](https://clawhub.ai/user/durtydhiana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up persistent memory folders, templates, wake routines, feedback logs, and search workflows so agents can retain decisions, procedures, and recent context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory logs can contain sensitive project, credential, or personal context.

Mitigation: Keep the memory folder private and redact secrets or credentials before storing entries.

Risk: Optional setup steps may alter shell profiles, local files, or repository state.

Mitigation: Review AGENTS.md, HEARTBEAT.md, shell profile, chmod, git pull, and rm commands before applying them.

Risk: Persisted memory can become stale or misleading over time.

Mitigation: Treat stored memory as helpful context to verify, not as authoritative instructions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/durtydhiana/skills/agent-memory-kit-2-1-0)
- [Publisher profile](https://clawhub.ai/user/durtydhiana)
- [README](artifact/README.md)
- [Search and Recall documentation](artifact/SEARCH.md)
- [Installation guide](artifact/INSTALLATION.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON search output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file templates, local setup steps, wake-routine guidance, and search command patterns for an agent memory workflow.]

## Skill Version(s):

2.1.0 (source: artifact/_meta.json and CHANGELOG.md; ClawHub release version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
