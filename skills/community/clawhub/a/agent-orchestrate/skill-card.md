## Description:

Multi-agent orchestration patterns for OpenClaw, including quick-reference guidance for spawning sub-agents, parallel work, and basic coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltenbot000](https://clawhub.ai/user/moltenbot000)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to plan simple multi-agent workflows, including fan-out, pipeline, dependency-tree, human-checkpoint, and supervisor patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prior agent results can be incorrect or untrusted when passed into later orchestration stages.

Mitigation: Review intermediate results before reuse and require human approval before sensitive changes or external sends.

Risk: Spawned agents may receive broader tool access than a subtask requires.

Mitigation: Limit available tools and scope each spawned agent to one clear task.

Risk: State and checkpoint files can expose private task content or secrets.

Mitigation: Avoid storing secrets or sensitive content in orchestration state, and restrict or remove checkpoint files when no longer needed.

Risk: Long-running or stuck agents can consume unnecessary resources.

Mitigation: Set timeouts, poll at reasonable intervals, and stop or retry failed agents deliberately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltenbot000/skills/agent-orchestrate)
- [Fan-Out Pattern](references/fan-out.md)
- [Pipeline Pattern](references/pipeline.md)
- [Dependency Tree Pattern](references/dependency-tree.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples should be adapted and reviewed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
