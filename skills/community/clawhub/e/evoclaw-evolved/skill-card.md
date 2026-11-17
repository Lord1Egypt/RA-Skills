## Description:

EvoClaw (Evolved) helps an agent maintain and evolve its identity by logging experiences, classifying significance, reflecting, proposing governed SOUL.md changes, and validating the pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuoyu017](https://clawhub.ai/user/shuoyu017)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use EvoClaw to install an experience-to-reflection pipeline that records interaction evidence, classifies significance, and routes proposed identity changes through configurable governance before updating SOUL.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad persistent authority over memory, agent instructions, credentials, network activity, and SOUL.md edits with unsafe controls.

Mitigation: Install only in a non-sensitive workspace, keep governance supervised, and review proposed identity or instruction changes before they are applied.

Risk: External feeds, telemetry or config sync, and the visualizer can expose workspace or operational data.

Mitigation: Disable external feeds and telemetry unless required, use environment variable names instead of pasted secrets, and avoid the visualizer until it is localhost-only, authenticated, and routed through the proposal pipeline.

Risk: Instruction rewrites and fork cleanup can alter agent behavior or workspace state.

Mitigation: Review installation diffs, scan before deployment, and require human approval for instruction rewrites and cleanup actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuoyu017/skills/evoclaw-evolved)
- [README.md](artifact/README.md)
- [configure.md](artifact/configure.md)
- [EvoClaw Data Schemas Reference](artifact/references/schema.md)
- [EvoClaw Pipeline Examples](artifact/references/examples.md)
- [EvoClaw Source API Reference](artifact/references/sources.md)
- [Heartbeat Debugging Guide](artifact/references/heartbeat-debug.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JSONL, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation, governance, validation, and troubleshooting guidance for agent-managed identity evolution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
