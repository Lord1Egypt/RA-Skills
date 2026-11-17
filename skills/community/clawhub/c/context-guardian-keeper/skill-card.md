## Description:

Context Guardian helps autonomous AI agents preserve long-running task continuity with durable checkpoints, structured summaries, restart recovery, pressure-aware trimming, and safe stops before context loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent platform engineers use this skill to add durable task state, compact recovery summaries, context-pressure checks, and halt behavior to autonomous agent loops that may outlive one LLM context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local checkpoint and summary files may contain sensitive task details if the host writes secrets or raw outputs into durable state.

Mitigation: Use a dedicated state directory with limited permissions and avoid storing secrets or sensitive raw outputs in task state or summaries.

Risk: Context-pressure decisions can be unreliable if a production host relies on fallback estimation instead of host-owned pressure reporting.

Mitigation: Integrate an explicit numeric context-pressure signal and reserve the character-based estimator for reference or test environments.

Risk: Agents may resume from stale or ambiguous recovery data after context loss.

Mitigation: Read the durable task state and latest summary before each major action, stop on missing state, and resume only from a non-empty next_action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ciklopentan/skills/context-guardian-keeper)
- [Task State Schema](references/task-state-schema.md)
- [Summary Template](references/summary-template.md)
- [Configuration Example](references/config-example.yaml)
- [Integration Checklist](references/integration-checklist.md)
- [Implementation Notes](references/implementation-notes.md)
- [Persisted Task State Example](references/persisted-task-state.example.json)
- [Summary Example](references/summary-example.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON state files, markdown summaries, Python reference code, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local checkpoint and summary artifacts under host-configured paths; production hosts should provide explicit numeric context-pressure values.]

## Skill Version(s):

1.1.7 (source: server release metadata and packaging checklist)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
