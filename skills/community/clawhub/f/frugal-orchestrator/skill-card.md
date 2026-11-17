## Description:

Token-efficient task orchestration system that delegates work to specialized subordinates while prioritizing system-level solutions over AI inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelohenriq](https://clawhub.ai/user/nelohenriq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route work across system commands, scripts, cached results, delegated agents, batch workers, and scheduled tasks to reduce token use and execution cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manifest-controlled tasks can run shell commands and scripts.

Mitigation: Install in a sandbox or low-privilege account, review task manifests before execution, and use dry-run mode for new manifests.

Risk: Delegation context, logs, cache entries, metrics, and scheduled tasks may persist task data.

Mitigation: Avoid passing secrets or sensitive prompts until retention and redaction behavior is clear, and review generated logs, cache files, and scheduled tasks.

Risk: Automation can create scheduled tasks and includes git commit and push behavior.

Mitigation: Review scheduled task definitions and git automation before enabling recurring or repository-writing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nelohenriq/skills/frugal-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/nelohenriq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON status objects, TOON metrics, shell commands, and Python configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local cache, log, metric, and scheduled-task files during use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
