## Description:

Checks whether Chinese calendar dates are statutory holidays, adjusted workdays, ordinary weekends, or workdays using the chinesecalendar Python package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuehongyanl](https://clawhub.ai/user/xuehongyanl)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to answer China holiday and adjusted workday questions or to gate reminder workflows before scheduled jobs run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party Python package.

Mitigation: Install in an isolated Python environment, review or pin the chinesecalendar package version when supply-chain control matters, and treat dependency upgrades as user-approved maintenance.

Risk: Holiday data can be unavailable for unsupported far-past or far-future years, and repeated package upgrades may not resolve that.

Mitigation: Limit date queries to the supported year range, return an unsupported-year response for out-of-range dates, and avoid repeated upgrade attempts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuehongyanl/skills/check-chinese-holiday)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; optional JSON results from check.py.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the chinesecalendar Python package and bounded date queries near supported calendar-data years.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
