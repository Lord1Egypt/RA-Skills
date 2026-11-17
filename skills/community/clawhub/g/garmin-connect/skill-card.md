## Description:

Garmin Connect integration for Clawdbot: sync fitness data (steps, HR, calories, workouts, sleep) every 5 minutes using OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayleigh3105](https://clawhub.ai/user/rayleigh3105)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to authenticate with Garmin Connect, sync local fitness data into Clawdbot workflows, and format daily activity, sleep, and workout metrics for agent-readable use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin account credentials, OAuth session tokens, and sensitive health data stored on disk.

Mitigation: Review the authentication flow before use, avoid entering a real password on the command line, and restrict permissions on ~/.garth and ~/.clawdbot files.

Risk: Developer-specific paths, email examples, cache files, and log paths may expose private data or fail in another environment.

Mitigation: Replace hard-coded local paths and example account identifiers before deployment, and configure private cache and log locations.

Risk: A 5-minute cron sync can repeatedly access Garmin data and write local logs or cache files.

Mitigation: Enable scheduled sync only after confirming storage locations, file permissions, and logging behavior are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rayleigh3105/skills/garmin-connect)
- [Clawdbot](https://clawd.bot)
- [Garmin SSO sign-in](https://sso.garmin.com/sso/signin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and Python examples; scripts output JSON cache data and formatted text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Garmin OAuth session and cache files; sync output includes activity, sleep, and workout metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
