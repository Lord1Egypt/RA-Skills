## Description:

Production-grade multi-agent orchestration patterns for decomposing complex tasks into parallel subtasks, coordinating agent swarms, building sequential pipelines, and running review cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipstark](https://clawhub.ai/user/philipstark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to plan and coordinate multi-agent workflows for code changes, research, content creation, DevOps checks, and quality review. It helps an agent select fan-out, pipeline, swarm, or review-cycle patterns and produce structured task plans, prompts, configuration examples, and orchestration reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to coordinate multiple workers that read or modify project files.

Mitigation: Use explicit file scopes, file ownership, and review gates before accepting changes.

Risk: The skill can guide agents to run tests or shell commands as part of orchestration.

Mitigation: Require approval for Bash, test, deployment, and other environment-changing commands before execution.

Risk: Parallel workers may consume excessive budget or continue beyond the intended task scope.

Mitigation: Set max concurrency, per-agent budgets, total budgets, timeouts, and max-turn limits before launching workers.

Risk: Workers may encounter secrets or credentials while reading project files.

Mitigation: Block access to secret-bearing files such as .env, keys, PEM files, and credential stores.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/philipstark/skills/fl-multi-agent-orchestrator)
- [claude-swarm](https://github.com/affaan-m/claude-swarm)
- [claude_code_agent_farm](https://github.com/mckaywrigley/claude_code_agent_farm)
- [TubeFlow](https://github.com/webnestify/tubeflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, YAML, prompt, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create .orchestrator artifacts, execution plans, task summaries, review reports, and budget or status summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
