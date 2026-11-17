## Description:

Event Orchestrator helps agents coordinate multi-skill workflows with event publishing and subscription, middleware processing, and task state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to coordinate event-driven multi-skill workflows, route events through middleware, and track orchestration task state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene issues may affect CI or production use.

Mitigation: Refresh and review the locked development dependencies before CI or release use.

Risk: The built-in rate limiter should not be relied on as a security control until the middleware dispatch bug is fixed.

Mitigation: Patch and test middleware dispatch, then add explicit rate-limit regression coverage before depending on it.

Risk: Untrusted configuration or source inputs may expand risk before the reported issues are patched.

Mitigation: Use trusted local configuration and source files only, and isolate evaluation from sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/event-orchestrator)
- [README](artifact/README.md)
- [Evaluation report](artifact/docs/evaluation-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for in-process Node.js event orchestration and task-state workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
