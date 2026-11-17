## Description:

Multi-agent orchestration with 5 proven patterns - Work Crew, Supervisor, Pipeline, Council, and Auto-Routing

This skill is ready for commercial/non-commercial use.

## Publisher:

[variable190](https://clawhub.ai/user/variable190)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate OpenClaw sub-agents for parallel research, dynamic supervision, staged pipelines, expert-style review, and task routing when single-agent work is too brittle or slow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill spawns multiple OpenClaw sessions, which can expand tool use, cost, and operational impact.

Mitigation: Review the task before execution, keep host permissions limited, and use multi-agent patterns only for work where the reliability or speed gain justifies the extra token and session cost.

Risk: Task text and generated previews may be persisted in local state files.

Mitigation: Avoid putting secrets or sensitive business data in task text, keep safe-state mode enabled, and rely on redacted state previews unless debugging in a controlled environment.

Risk: Prompt injection or unsafe task propagation cannot be fully eliminated in spawned-agent workflows.

Mitigation: Keep tasks scoped and explicit, review generated outputs before high-impact actions, and use the documented sanitization and safety-boundary controls.

Risk: The council workflow is reported by security evidence as returning simulated expert results instead of collected agent outputs in one advertised path.

Mitigation: Do not use council output as real expert consensus until that path is fixed or clearly treated as demo-only; verify decisions with qualified reviewers for high-stakes use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/variable190/skills/agent-orchestrator-molter)
- [Skill README](artifact/README.md)
- [Security Notes](artifact/SECURITY.md)
- [Example Workflows](artifact/examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured CLI output, often with shell commands or JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn multiple OpenClaw sessions and aggregate or synthesize their results; token use can be much higher than single-agent execution.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
