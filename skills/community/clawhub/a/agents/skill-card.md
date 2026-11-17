## Description:

Agents helps developers design, debug, evaluate, and harden framework-agnostic AI agents, including loops, tools, memory, context budgets, cost controls, escalation, security, and production rollout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, debug, evaluate, secure, and operate AI agents. It provides guidance for agent loop design, tool schemas, memory strategy, cost and latency controls, evals, human approval, and production readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain persistent local records and migrate legacy agent folders automatically.

Mitigation: Install only where persistent local memory is acceptable, and require explicit approval before writes, deletions, or migrations.

Risk: The skill may read shared project, server, finance, contact, and profile notes under configured Clawic data paths.

Mitigation: Use it only in environments where those local records are appropriate context, and review access expectations before installation.

Risk: Credential-related material could be encountered while designing agents or processing pasted configuration.

Mitigation: Store credential pointers only, never secret values, and strip secrets from prompts, environment files, traces, and tool configuration before saving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/agents)
- [Clawic Agents skill page](https://clawic.com/skills/agents)
- [Architecture guidance](artifact/architecture.md)
- [Tool design guidance](artifact/tools.md)
- [Memory design guidance](artifact/memory-design.md)
- [Evaluation guidance](artifact/evaluation.md)
- [Security guidance](artifact/security.md)
- [Production guidance](artifact/production.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional code blocks, shell commands, tables, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local agent notes under configured Clawic data paths when used as an installed skill.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
