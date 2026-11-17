## Description:

Cost Optimizer helps OpenClaw and Claude Code users reduce token spend with model-routing recommendations, context compression, heartbeat tuning, usage reporting, and optimized configuration generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze agent usage costs, choose lower-cost models for appropriate tasks, compress long working context, tune heartbeat behavior, and generate cost-aware configuration proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read global OpenClaw or Claude Code settings and usage logs from the user's home directory.

Mitigation: Run it only when those files are intended inputs, and avoid global configuration reads unless they are needed for the task.

Risk: Context compression can persist recent prompts, code, tool output, or secrets in a project-local .context-snapshot.md file.

Mitigation: Review snapshot contents before sharing, add snapshot files to .gitignore, and remove sensitive data from generated snapshots.

Risk: Generated routing or heartbeat configuration can change model choice, cost, latency, and answer quality.

Mitigation: Review generated configuration and diffs before applying them, and use conservative or balanced presets for sensitive workflows.

## Reference(s):

- [Cost Optimizer Skill Page](https://clawhub.ai/fullstackcrew-alpha/skills/cost-optimizer)
- [Model Pricing Reference](references/model-pricing.md)
- [Routing Rules Reference](references/routing-rules.md)
- [OpenClaw](https://openclaw.dev)
- [OpenClaw Config Schema](https://openclaw.dev/schema/config.json)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, JSON configuration snippets, shell commands, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate project-local context snapshots and optimized OpenClaw or Claude Code configuration proposals.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
