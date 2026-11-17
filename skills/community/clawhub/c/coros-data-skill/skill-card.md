## Description:

Queries COROS running activity data for a configured COROS account by logging in and fetching outdoor, indoor, trail, and treadmill running records for a date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wurongle](https://clawhub.ai/user/wurongle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve COROS running activities and compute simple running-distance summaries from their own account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses private COROS account activity data.

Mitigation: Install only when account activity access is acceptable, and run it in an environment limited to the intended COROS account.

Risk: COROS_PASSWORD is a reusable password-derived secret and may be printed or committed if handled casually.

Mitigation: Store the value in protected environment variables or a secret manager, avoid printing it, do not commit scripts/.env, and rotate the COROS password if the hash is exposed.

Risk: The JavaScript dependency lockfile should be reviewed before sensitive use.

Mitigation: Review or update npm dependency and lockfile provenance before deploying in a sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wurongle/skills/coros-data-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/wurongle)
- [COROS training dashboard](https://trainingcn.coros.com/admin/views/activities)
- [COROS login endpoint](https://teamcnapi.coros.com/account/login)
- [COROS activity query endpoint](https://teamcnapi.coros.com/activity/query)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript examples and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces COROS activity records and distance summaries through JavaScript helper functions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
