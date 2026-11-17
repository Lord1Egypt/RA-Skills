## Description:

Retrieves and summarizes COROS running account data, including dashboard status, activity history, activity details, training load, schedules, and goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doaspx](https://clawhub.ai/user/doaspx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a configured COROS account for running-data review, training recap, schedule and goal inspection, and optional schedule changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive COROS fitness account data and stores session secrets in local configuration.

Mitigation: Keep demo mode enabled until configuration is intentional, protect config.json as a secret, and do not commit or share local account, token, or cookie values.

Risk: Training schedule write features can update or delete COROS training schedules.

Mitigation: Leave schedule_write.auto_apply set to false unless the exact schedule action and target have been reviewed and accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doaspx/skills/coros-skill)
- [COROS web app](https://t.coros.com/)
- [COROS API base](https://teamcnapi.coros.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with command-line output and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make authenticated COROS API calls and may write session tokens or cookies to local config; schedule writes remain preview-only unless auto_apply is enabled.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
