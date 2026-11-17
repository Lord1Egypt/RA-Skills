## Description:

Schedule recurring AI agent prompts using intervals or cron expressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Acp Loop to schedule recurring agent prompts for monitoring, reporting, cleanup, and other periodic workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install a mutable global npm CLI.

Mitigation: Review the npm package and version before installation and avoid elevated privileges.

Risk: Recurring agent prompts can continue indefinitely and repeat actions without strong boundaries.

Mitigation: Use bounded schedules such as `--max` or `--timeout`, and prefer read-only or dry-run prompts for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/femto/skills/acp-loop)
- [GitHub repository](https://github.com/femto/acp-loop)
- [npm package](https://www.npmjs.com/package/acp-loop)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
