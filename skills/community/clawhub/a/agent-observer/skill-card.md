## Description:

Agent Observer tracks the activity, output quality, and possible inactivity of the named InStreet agents Baihu (snow_tiger) and Fenghuang (fenghuang).

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to run recurring status checks for two named InStreet agents and produce structured daily or weekly observation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring observation of named agents can expose private or unauthorized activity data.

Mitigation: Use the skill only with authorization to monitor the named agents and access the relevant InStreet status data or logs.

Risk: Heartbeat or recurring reports can create opaque monitoring if configured without notice.

Mitigation: Configure recurring scans and reports visibly, and do not apply them to private logs, personal accounts, or additional agents without explicit approval.

Risk: Inactivity reports can be inaccurate when platform status, API availability, or timestamp data is wrong.

Mitigation: Follow the skill's false-inactivity checklist before escalating an agent as inactive or lost contact.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured observation summaries and incident-style reports for the named agents.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
