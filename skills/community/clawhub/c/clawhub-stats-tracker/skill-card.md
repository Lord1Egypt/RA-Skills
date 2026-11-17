## Description:

ClawHub Stats Tracker helps agents query public ClawHub skill operating metrics, including stars, downloads, installs, versions, and publish times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub skill publishers use this skill to check release statistics for tracked skills, individual skill slugs, or slug series. It supports operational reporting for public ClawHub releases without requiring ClawHub login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted tracked-skills configuration can lead the helper script to execute unsafe local code.

Mitigation: Use only a trusted ~/.clawhub/tracked-skills.json file and validate slug values before running batch lookups.

Risk: The helper script invokes a mutable npm package at runtime.

Mitigation: Pin the clawhub CLI version before running the script in production or repeatable reporting workflows.

Risk: Downloads and installs metrics are documented as potentially inaccurate.

Mitigation: Treat install and download counts as operational indicators and corroborate important decisions with ClawHub issue status or other records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/clawhub-stats-tracker)
- [OpenClaw ClawHub installs metrics issue](https://github.com/openclaw/clawhub/issues/156)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and tabular text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read a local tracked-skills JSON file and call the public clawhub inspect command for each slug.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
