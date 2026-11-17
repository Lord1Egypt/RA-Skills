## Description:

Create and manage automation workflows for repetitive tasks. Use when user needs to schedule periodic data sync, chain API calls, set up triggered actions, build if-this-then-that style automation, or create multi-step business workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to define YAML workflows for scheduled jobs, API call chains, webhook-style actions, notifications, transformations, and data sync tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended workflow execution can send requests or messages to destinations defined by workflow files.

Mitigation: Review workflow files before execution and use explicit allowlists for network destinations.

Risk: Workflow actions may expose environment secrets when broad environment variables are available.

Mitigation: Run with the minimum required environment and avoid exposing secrets unless the workflow and destination are trusted.

Risk: Weakened HTTPS verification can reduce protection for network requests.

Mitigation: Require HTTPS verification before using the skill with secrets or business data.

Risk: Daemon mode can run workflows repeatedly without close supervision.

Mitigation: Avoid daemon mode until scheduling behavior is reviewed and constrained.

## Reference(s):

- [Automation Workflow Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/flow-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML examples, Python commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create workflow files and run the bundled workflow script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
