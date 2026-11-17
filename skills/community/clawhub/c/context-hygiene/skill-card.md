## Description:

Reasoning hygiene protocol for OpenClaw agents - keep context sharp by collapsing exploration into decisions, enforcing file budgets, and pruning ghost context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppiankov](https://clawhub.ai/user/ppiankov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw workspace context concise by collapsing exploration notes into decisions, pruning stale memory, and setting practical file budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context pruning can remove useful memory notes or workspace context.

Mitigation: Ask the agent to show diffs before deleting memory, and back up important notes before pruning.

Risk: Cron reports, reminders, and date references can be wrong if the agent uses an incorrect timezone.

Mitigation: Confirm the user's real timezone and record it explicitly before relying on time-sensitive automation.

Risk: The optional validator command installs and runs an external package.

Mitigation: Run the validator only after verifying that the installed package is trusted for the workspace.

## Reference(s):

- [Agent-Native CLI Convention](https://ancc.dev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides workspace memory budgets, pruning rules, session lifespan guidance, and a context hygiene self-check.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
