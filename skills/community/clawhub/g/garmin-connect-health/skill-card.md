## Description:

Fetch health and fitness data from Garmin Connect -- 40+ metrics including sleep, HRV, stress, body battery, SpO2, VO2 Max, training status, and activities. Stores data locally as JSON and SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dw1161](https://clawhub.ai/user/dw1161)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent fetch, cache, and analyze their Garmin Connect health and fitness metrics from a local machine. It supports daily summaries, sleep, HRV, stress, Body Battery, SpO2, training readiness, activities, and queryable local storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a Garmin account and stores detailed health data on the local machine.

Mitigation: Install only for accounts and machines where local storage of this data is acceptable, and keep GARMIN_DATA_DIR and GARMIN_TOKENSTORE private and out of shared or synced folders.

Risk: Credentials can be provided through CLI arguments, environment variables, macOS Keychain, or a local credentials file.

Mitigation: Prefer macOS Keychain over CLI passwords or ~/.garmin_credentials, and avoid command-line passwords that may appear in shell history or process listings.

Risk: The skill depends on the garminconnect package for authentication and Garmin Connect access.

Mitigation: Consider pinning and reviewing the garminconnect dependency before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dw1161/skills/garmin-connect-health)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or SQLite-backed health data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local daily JSON snapshots, a latest JSON snapshot, and a SQLite database for daily summaries, activities, and activity sets.]

## Skill Version(s):

1.1.0 (source: frontmatter, skill.json, changelog released 2026-08-20, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
