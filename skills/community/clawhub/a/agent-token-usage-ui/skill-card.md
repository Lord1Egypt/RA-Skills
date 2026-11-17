## Description:

This deprecated package directs users to migrate from Agent Token Usage UI to the main agent-token-usage skill and run its UI setup script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this deprecated skill as a migration notice for replacing agent-token-usage-ui with agent-token-usage and applying its UI integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deprecated skill directs users to install and run a replacement skill script that creates a persistent launchd refresh job.

Mitigation: Review the replacement skill's apply-ui.sh and remove-ui.sh, confirm the exact replacement version, and understand how to remove the launchd job before running the migration command.

Risk: This package is deprecated and will receive no further updates.

Mitigation: Uninstall agent-token-usage-ui and use the maintained agent-token-usage skill for the UI button, modal, and refresh job.

## Reference(s):

- [Agent Token Usage UI ClawHub page](https://clawhub.ai/symbolstar/skills/agent-token-usage-ui)
- [Agent Token Usage replacement skill](https://clawhub.com/skills/agent-token-usage)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deprecated migration notice; no maintained functionality remains in this package.]

## Skill Version(s):

0.9.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
