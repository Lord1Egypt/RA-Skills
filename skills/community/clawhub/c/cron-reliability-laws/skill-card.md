## Description:

Hard rules for Cron reliability: Shell-First architecture, mandatory wrappers (flock/logging), and LLM constraints to prevent timeouts and token-waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rwesmarter](https://clawhub.ai/user/rwesmarter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as guidance for designing reliable cron and scheduled tasks, especially when deciding when to use deterministic shell wrappers, locking, logging, alerting, and constrained LLM usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cron wrapper or scheduled-task configuration could mishandle .env loading, log contents, alert destinations, or cron persistence if applied without review.

Mitigation: Review generated shell wrappers and configuration before use, with attention to .env handling, log contents, alert destinations, and cron persistence.

Risk: Cron guidance may be applied to tasks that are better handled by higher-level reasoning instead of deterministic success/failure logic.

Mitigation: Use deterministic scripts for binary or data-driven outcomes and reserve LLM use in scheduled tasks for high-level reasoning with constrained context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rwesmarter/skills/cron-reliability-laws)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional inline shell, cron, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code; review generated wrappers and scheduled-task configuration before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
