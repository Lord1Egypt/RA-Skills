## Description: <br>
Production-ready context continuity skill for autonomous AI agents. Use when tasks may outlive a single LLM context window, when you need durable checkpoints, structured summaries, restart recovery, pressure-aware trimming, or when the agent must stop safely instead of continuing blindly after context loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-integration engineers use this skill to add durable checkpoints, structured summaries, restart recovery, and pressure-aware halt behavior to long-running autonomous agent tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves task state and summaries to disk, which can expose local task history or sensitive details if goals, summaries, or checkpoints contain secrets. <br>
Mitigation: Install only where local task-history persistence is acceptable, keep the configured context path inside the intended project, avoid putting secrets in goals or summaries, review retention practices for .context_guardian, and use stronger file permissions on shared machines. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Task State Schema](references/task-state-schema.md) <br>
- [Summary Template](references/summary-template.md) <br>
- [Integration Checklist](references/integration-checklist.md) <br>
- [Implementation Notes](references/implementation-notes.md) <br>
- [Configuration Example](references/config-example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON task state, Markdown summaries, status strings, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local checkpoint and summary artifacts when integrated with a host filesystem.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata and packaging checklist) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
