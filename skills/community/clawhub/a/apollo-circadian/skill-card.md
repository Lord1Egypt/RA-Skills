## Description:

Helps an agent align work timing with a circadian schedule by reporting the current phase, recommending task types, and suggesting when to defer deep work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent assess the current time against a configured circadian schedule, recommend suitable work types, and flag low-energy or maintenance windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad heartbeat and time-related triggers may cause the agent to apply scheduling guidance when the user did not explicitly request it.

Mitigation: Review trigger configuration before deployment and require clear user or workspace policy approval before deferring active work.

Risk: Late-night or maintenance windows may lead the agent to pause non-emergency tasks or suggest invoking another workflow.

Mitigation: Treat workflow invocation as advisory unless the deployment policy explicitly permits automatic handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-circadian)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style status report with optional shell command output and JSON state fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports circadian phase, recommended task category, efficiency match, time until next phase, and optional maintenance-window guidance.]

## Skill Version(s):

2.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
