## Description:

GH Monitor helps agents monitor GitHub repositories for issues, pull requests, CI runs, new activity, label filters, and scheduled notifications through GitHub CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deliverydriver](https://clawhub.ai/user/deliverydriver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and repository operators use this skill to ask an agent for GitHub issue, pull request, and CI status monitoring with optional label filters and scheduled alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use an existing GitHub CLI session against an unintended repository or scope.

Mitigation: Confirm GitHub CLI authentication, the target owner/repository, labels, and intended permissions before running monitoring commands.

Risk: Recurring checks can send unwanted or stale notifications if the cron schedule or message target is wrong.

Mitigation: Review the cron expression, payload, notification destination, and stop condition before enabling scheduled monitoring.

Risk: The artifact references support files and a related gh-issues skill that are not included in the package.

Mitigation: Verify those dependencies are available in the target agent environment or adapt the workflow to the included GitHub CLI command reference.

## Reference(s):

- [GH Commands](references/gh-commands.md)
- [ClawHub skill page](https://clawhub.ai/deliverydriver/skills/gh-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline GitHub CLI and cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory monitoring steps and command suggestions; execution depends on the agent environment, GitHub CLI authentication, and any configured scheduler or messaging tool.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
