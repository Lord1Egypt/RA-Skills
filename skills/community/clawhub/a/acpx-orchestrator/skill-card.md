## Description:

Enhanced terminal AI agent orchestrator with parallel execution, health checks, and workflow presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qriiz112](https://clawhub.ai/user/qriiz112)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use ACP Orchestrator to coordinate terminal AI agents for discovery, health checks, single-agent tasks, parallel or sequential batch execution, preset review/refactor/test/debug workflows, and JSON-formatted runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates core behavior to npm packages without pinned versions.

Mitigation: Verify and pin acceptable npm package versions before installing or running the orchestrator.

Risk: Parallel, batch, and passthrough commands can execute task files or prompts from untrusted sources.

Mitigation: Use only trusted task files and prompts, and review commands before execution.

Risk: Invoked agents may inherit the same file, tool, and credential access as the normal agent environment.

Mitigation: Run the orchestrator in a constrained workspace with only the files and credentials needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qriiz112/skills/acpx-orchestrator)
- [Publisher profile](https://clawhub.ai/user/qriiz112)
- [Project repository listed in manifest](https://github.com/qriiz112/acpx-orchestrator)
- [Quick reference](artifact/COMPARISON.md)
- [Example batch tasks](artifact/examples/tasks-example.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke external terminal agents and can request JSON output through the acpx CLI.]

## Skill Version(s):

4.0.1 (source: server release metadata; artifact metadata reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
