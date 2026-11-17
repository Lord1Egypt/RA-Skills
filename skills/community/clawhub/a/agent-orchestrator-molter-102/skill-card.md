## Description:

Multi-agent orchestration with 5 proven patterns - Work Crew, Supervisor, Pipeline, Council, and Auto-Routing

This skill is ready for commercial/non-commercial use.

## Publisher:

[variable190](https://clawhub.ai/user/variable190)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to coordinate OpenClaw sub-agents for parallel research, supervisor-led decomposition, staged pipelines, expert councils, and task routing when a single-agent workflow is brittle or slow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agent orchestration forwards task content into spawned OpenClaw sessions, which can expose sensitive input if users include secrets.

Mitigation: Do not use the skill with secrets or sensitive material unless the OpenClaw runtime is tightly sandboxed and least-privilege controls are in place.

Risk: Prompt-injection attempts in task text may still influence workers even with sanitization and a safety preamble.

Mitigation: Keep tasks scoped and explicit, review generated outputs before high-impact use, and run new workflow prompts in a sandbox or test environment first.

Risk: Council mode can launch sub-agent sessions while returning simulated expert opinions rather than collected sub-agent deliberation.

Mitigation: Treat council-mode results as advisory and verify them independently before making important decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/variable190/skills/agent-orchestrator-molter-102)
- [Agent Orchestrator README](README.md)
- [Security Notes](SECURITY.md)
- [Pipeline Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, or JSON depending on the selected orchestration command and output flag]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May spawn multiple OpenClaw sub-agent sessions and can use substantially more tokens than a single-agent run.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
