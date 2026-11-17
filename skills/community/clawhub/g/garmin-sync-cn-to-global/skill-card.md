## Description:

Sync activities from Garmin China to Garmin Global using local timestamps and distance to avoid duplicates in a one-way sync process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamtonyzhou](https://clawhub.ai/user/iamtonyzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Garmin users use this skill to configure and run a one-way synchronization from Garmin China to Garmin Global while avoiding duplicate activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin CN and Global account passwords may be stored locally in plaintext.

Mitigation: Use a dedicated Garmin password where possible, restrict ~/.config/garmin-sync permissions, avoid exposing passwords in shell history, and rotate or remove credentials when no longer using the skill.

Risk: The release is marked suspicious because of credential storage and weak local file handling.

Mitigation: Run it only from a private user account or virtual environment and review the code before using primary Garmin credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying sync workflow may store Garmin CN and Global credentials locally in plaintext and should be reviewed before use.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
